from src.database import db_manager
from src.logger import logger
import time
import json

TITLE_EFFECTS = {
    "title_sword_fairy": {"name": "[剑仙]", "desc": "基础修为获取 +5%", "buff": {"exp_mult": 0.05}},
    "title_time_rewind": {"name": "[时光回溯]", "desc": "心魔增长几率 -1%", "buff": {"mind_resist": 0.01}},
    "title_focus":       {"name": "[入定]", "desc": "基础修为获取 +2%", "buff": {"exp_mult": 0.02}},
    "title_night_walker":{"name": "[夜游神]", "desc": "夜间(22:00-04:00) 掉落率 +10%", "buff": {"drop_mult": 0.10, "cond_hour_start": 22, "cond_hour_end": 4}},
    "title_merchant":    {"name": "[精算师]", "desc": "物品出售价格 +5%", "buff": {"sell_mult": 0.05}},
    "title_rich":        {"name": "[多宝道人]", "desc": "灵石获取 +5%", "buff": {"money_mult": 0.05}},
    "title_lucky_son":   {"name": "[气运之子]", "desc": "全局掉落率 +5%", "buff": {"drop_mult": 0.05}},
    "title_stone":       {"name": "[顽石]", "desc": "渡劫失败惩罚减少 5%", "buff": {"proto_shield": 0.05}},
    "title_resilient":   {"name": "[百折不挠]", "desc": "心魔自然衰减速度 +10%", "buff": {"mind_decay": 0.10}},
}

class AchievementManager:
    def __init__(self):
        self.cached_achievements = []
        self.last_check_time = 0
        self.check_interval = 60 # Check every minute

    def get_all_achievements(self):
        """
        Return list of dicts: {id, name, desc, status, progress_str, reward_desc}
        """
        try:
            with db_manager._get_conn() as conn:
                conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM achievements ORDER BY status DESC, id ASC")
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to fetch achievements: {e}")
            return []

    def get_title_effect(self, title_id):
        return TITLE_EFFECTS.get(title_id, None)

    def check_periodic(self, cultivator):
        """
        Periodically check for achievements based on aggregated stats.
        Should be called every ~60s from main loop.
        """
        if time.time() - self.last_check_time < self.check_interval:
            return []
        
        self.last_check_time = time.time()
        new_unlocks = []

        # 1. Fetch Aggregated Stats
        stats = self._fetch_global_stats()
        
        # 2. Add Cultivator State
        stats['money'] = cultivator.money
        stats['inventory_fullness'] = len(cultivator.inventory) # Simple count for now, logic calls for %?
        # Assuming bag size is soft-capped or we just use item count
        
        # 3. Check Locked Achievements
        try:
            with db_manager._get_conn() as conn:
                conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM achievements WHERE status = 0")
                locked_achs = cursor.fetchall()
                
                for ach in locked_achs:
                    if self._evaluate(ach, stats, cultivator):
                        self._unlock(conn, ach['id'])
                        new_unlocks.append(ach)
                        
                conn.commit()
        except Exception as e:
            logger.error(f"Achievement check failed: {e}")
            
        return new_unlocks

    def check_trigger(self, cultivator, trigger_type, value=None):
        """
        Event-driven check (sell, event trigger, etc)
        """
        new_unlocks = []
        try:
            with db_manager._get_conn() as conn:
                conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
                cursor = conn.cursor()
                # Only check achievements with matching trigger type or relevant condition
                # Simplify: check all 'stat_total' is too slow? No, just check specific category?
                # Actually, iterate all locked is fine if count is small (<100)
                cursor.execute("SELECT * FROM achievements WHERE status = 0")
                locked_achs = cursor.fetchall()

                stats = self._fetch_global_stats() # Still need base stats for mixed conditions
                stats['money'] = cultivator.money
                
                # Manual override for trigger values
                if trigger_type == 'loot_tier_7':
                    stats['loot_tier_7'] = 1
                
                for ach in locked_achs:
                    if self._evaluate(ach, stats, cultivator):
                        self._unlock(conn, ach['id'])
                        new_unlocks.append(ach)
                
                conn.commit()
        except Exception as e:
            logger.error(f"Trigger check failed: {e}")
        return new_unlocks

    def claim_reward(self, cultivator, ach_id):
        """
        Claim reward for an unlocked achievement
        """
        try:
            with db_manager._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM achievements WHERE id = ?", (ach_id,))
                row = cursor.fetchone()
                # dict factory might not be set if we used _get_conn raw
                # safe to just map by index if we know schema, or set factory
                # Let's rely on fetchall from get_all_achievements for UI, here we careful.
                
                col_names = [col[0] for col in cursor.description]
                ach = dict(zip(col_names, row))

                if ach['status'] != 1:
                    return False, "Achievement not unlocked or already claimed"

                # Grant Reward
                msg = ""
                if ach['reward_type'] == 'item':
                    # Value format: "item_id:count"
                    parts = ach['reward_value'].split(':')
                    item_id = parts[0]
                    count = int(parts[1]) if len(parts) > 1 else 1
                    cultivator.gain_item(item_id, count)
                    item_name = cultivator.item_manager.get_item_name(item_id)
                    msg = f"获得物品: {item_name} x{count}"

                elif ach['reward_type'] == 'title':
                    title_id = ach['reward_value']
                    # Just unlock title availability (stored in achievement status=2)
                    # No extra inventory item needed, just the status change is enough.
                    eff = TITLE_EFFECTS.get(title_id, {})
                    title_name = eff.get('name', title_id)
                    msg = f"解锁称号: {title_name}"

                # Update Status to 2 (Claimed)
                cursor.execute("UPDATE achievements SET status = 2 WHERE id = ?", (ach_id,))
                conn.commit()
                
                return True, msg

        except Exception as e:
            logger.error(f"Claim reward failed: {e}")
            return False, f"系统错误: {e}"

    def _evaluate(self, ach, stats, cultivator):
        ctype = ach['condition_type']
        target = ach['condition_target']
        threshold = ach['threshold']

        val = 0
        if ctype == 'stat_total':
            val = stats.get(target, 0)
        elif ctype == 'stat_max':
            val = stats.get(target, 0)
        elif ctype == 'currency':
            val = stats.get('money', 0)
        elif ctype == 'currency_low':
            # Special: Money < Threshold AND Total Earned > 1000? 
            # Simplified: Money < Threshold AND Total Keys > 1000 (as proxy for playtime)
            curr = stats.get('money', 0)
            if curr < threshold and stats.get('keyboard', 0) > 1000:
                return True
            return False
        elif ctype == 'event_trigger':
             if target in stats and stats[target] >= threshold:
                 return True
        elif ctype == 'special':
            if target == 'inventory_fullness':
                # Threshold is %
                # Assume bag capacity is 100 slots? logic needed.
                # Current logic: cultivator.inventory size
                # Let's say max slots = 50 for now
                fullness = (len(cultivator.inventory) / 50) * 100
                val = fullness
            elif target == 'weekend_activity_hours':
                val = stats.get('weekend_hours', 0)
            elif target == 'afk_hours':
                # Hard to track specific AFK session max length without new logic
                # For now use max(active_minutes) inverse?
                # Placeholder: return False unless implemented
                return False
                
        return val >= threshold

    def _unlock(self, connection, ach_id):
        ts = int(time.time())
        connection.execute("UPDATE achievements SET status = 1, unlocked_at = ? WHERE id = ?", (ts, ach_id))
        logger.info(f"Achievement Unlocked: {ach_id}")

    def _fetch_global_stats(self):
        """
        Aggregates stats from activity_logs_minute
        Expensive query!
        """
        stats = {}
        try:
            with db_manager._get_conn() as conn:
                cursor = conn.cursor()
                
                # Basic sums
                cursor.execute("SELECT SUM(keys_count), SUM(mouse_count), COUNT(*) FROM activity_logs_minute")
                row = cursor.fetchone()
                stats['keyboard'] = row[0] or 0
                stats['mouse'] = row[1] or 0
                stats['uptime_minutes'] = row[2] or 0
                stats['uptime_hours'] = stats['uptime_minutes'] / 60
                
                # Max APM
                cursor.execute("SELECT MAX(keys_count + mouse_count) FROM activity_logs_minute")
                row = cursor.fetchone()
                stats['apm'] = row[0] or 0

                # Specific Keys (Need 'key_type' column which we DON'T have in simple schema)
                # We only have total keys. 
                # !!! Constraint: We cannot track 'Backspace' or 'Enter' specifically with current DB schema.
                # !!! Workaround: We can't implement 'ach_back_1k' properly without schema change in ActivityLog.
                # For now, we set them to 0 or mock them.
                # Let's Mock them as "Not Supported" or simply 0.
                stats['key_backspace'] = 0
                stats['key_enter'] = 0
                
                # Weekend Hours
                # SQLite strftime('%w') -> 0=Sunday, 6=Saturday
                cursor.execute("""
                    SELECT COUNT(*) FROM activity_logs_minute 
                    WHERE strftime('%w', timestamp, 'unixepoch', 'localtime') IN ('0', '6')
                """)
                row = cursor.fetchone()
                stats['weekend_hours'] = (row[0] or 0) / 60
                
        except Exception as e:
            logger.error(f"Global stats fetch error: {e}")
            
        return stats

achievement_manager = AchievementManager()

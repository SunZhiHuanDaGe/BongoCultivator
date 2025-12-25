import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import DB_FILE

ACHIEVEMENTS_DATA = [
    # 3.1 行道 (Dao of Action)
    {
        "id": "ach_kb_1w", "category": "action", "name": "剑意初成", 
        "desc": "累计敲击键盘超过 10,000 次", 
        "condition_type": "stat_total", "condition_target": "keyboard", "threshold": 10000,
        "reward_type": "item", "reward_value": "ore_iron_essence:1"
    },
    {
        "id": "ach_kb_100w", "category": "action", "name": "一剑开天门", 
        "desc": "累计敲击键盘 1,000,000 次", 
        "condition_type": "stat_total", "condition_target": "keyboard", "threshold": 1000000,
        "reward_type": "title", "reward_value": "title_sword_fairy" # [剑仙]
    },
    {
        "id": "ach_mouse_5w", "category": "action", "name": "指点江山", 
        "desc": "累计点击鼠标 50,000 次", 
        "condition_type": "stat_total", "condition_target": "mouse", "threshold": 50000,
        "reward_type": "item", "reward_value": "part_wolf_tooth:10"
    },
    {
        "id": "ach_apm_400", "category": "action", "name": "唯快不破", 
        "desc": "单分钟 APM 超过 400", 
        "condition_type": "stat_max", "condition_target": "apm", "threshold": 400,
        "reward_type": "item", "reward_value": "part_spider_silk:10"
    },
    {
        "id": "ach_back_1k", "category": "action", "name": "悔棋者", 
        "desc": "累计使用 Backspace 键 1,000 次", 
        "condition_type": "stat_total", "condition_target": "key_backspace", "threshold": 1000,
        "reward_type": "title", "reward_value": "title_time_rewind" # [时光回溯]
    },
    {
        "id": "ach_enter_5k", "category": "action", "name": "一锤定音", 
        "desc": "累计使用 Enter 键 5,000 次", 
        "condition_type": "stat_total", "condition_target": "key_enter", "threshold": 5000,
        "reward_type": "item", "reward_value": "ore_copper_red:5"
    },
    {
        "id": "ach_combo_1h", "category": "action", "name": "人键合一", 
        "desc": "持续操作 1 小时 (无超过 1 分钟的中断)", 
        "condition_type": "special", "condition_target": "combo_time", "threshold": 60, # minutes
        "reward_type": "title", "reward_value": "title_focus" # [入定]
    },

    # 3.2 岁月 (Dao of Time)
    {
        "id": "ach_time_24h", "category": "time", "name": "初窥门径", 
        "desc": "累计运行时间超过 24 小时", 
        "condition_type": "stat_total", "condition_target": "uptime_hours", "threshold": 24,
        "reward_type": "item", "reward_value": "pill_detox_0:1"
    },
    {
        "id": "ach_time_100h", "category": "time", "name": "沧海桑田", 
        "desc": "累计运行时间超过 100 小时", 
        "condition_type": "stat_total", "condition_target": "uptime_hours", "threshold": 100,
        "reward_type": "item", "reward_value": "stone_three_life:1"
    },
    {
        "id": "ach_work_late", "category": "time", "name": "守夜人", 
        "desc": "在凌晨 3:00-4:00 期间进行操作", 
        "condition_type": "special", "condition_target": "time_range_activity", "threshold": 1, 
        "reward_type": "title", "reward_value": "title_night_walker", # [夜游神]
        "is_hidden": 1
    },
    {
        "id": "ach_early_bird", "category": "time", "name": "闻鸡起舞", 
        "desc": "早晨 5:00-7:00 期间进行操作", 
        "condition_type": "special", "condition_target": "time_range_activity", "threshold": 1,
        "reward_type": "item", "reward_value": "water_dew_morning:5"
    },
    {
        "id": "ach_weekend", "category": "time", "name": "无休居士", 
        "desc": "周末累计操作超过 4 小时", 
        "condition_type": "special", "condition_target": "weekend_activity_hours", "threshold": 4,
        "reward_type": "item", "reward_value": "pill_strength_bary:2"
    },
    {
        "id": "ach_afk_long", "category": "time", "name": "神游太虚", 
        "desc": "连续挂机超过 2 小时无操作", 
        "condition_type": "special", "condition_target": "afk_hours", "threshold": 2,
        "reward_type": "title", "reward_value": "title_stone" # [顽石]
    },

    # 3.3 机缘 (Dao of Chance)
    {
        "id": "ach_evt_100", "category": "chance", "name": "红尘炼心", 
        "desc": "累计触发随机事件 100 次", 
        "condition_type": "stat_total", "condition_target": "events_triggered", "threshold": 100,
        "reward_type": "item", "reward_value": "pill_luck_minor:2"
    },
    {
        "id": "ach_fail_5", "category": "chance", "name": "道心弥坚", 
        "desc": "突破或渡劫失败累计 5 次", 
        "condition_type": "stat_total", "condition_target": "breakthrough_fails", "threshold": 5,
        "reward_type": "title", "reward_value": "title_resilient" # [百折不挠]
    },
    {
        "id": "ach_die_1", "category": "chance", "name": "兵解重修", 
        "desc": "因心魔爆炸或渡劫失败导致死亡一次", 
        "condition_type": "stat_total", "condition_target": "deaths", "threshold": 1,
        "reward_type": "item", "reward_value": "pill_reborn_heaven:1"
    },
    {
        "id": "ach_rare_drop", "category": "chance", "name": "天命所归", 
        "desc": "通过掉落获得 Tier 7 以上的物品", 
        "condition_type": "event_trigger", "condition_target": "loot_tier_7", "threshold": 1,
        "reward_type": "title", "reward_value": "title_lucky_son" # [气运之子]
    },
    {
        "id": "ach_trash_king", "category": "chance", "name": "垃圾佬", 
        "desc": "收集废品(Junk)类物品超过 50 个", 
        "condition_type": "item_count_category", "condition_target": "Junk", "threshold": 50,
        "reward_type": "item", "reward_value": "bag_storage_runes:1" # 假设有个扩容道具
    },
    {
        "id": "ach_monster_sl", "category": "chance", "name": "除魔卫道", 
        "desc": "累计处于战斗状态(Combat)超过 10 小时", 
        "condition_type": "stat_total", "condition_target": "combat_hours", "threshold": 10,
        "reward_type": "item", "reward_value": "beast_core_gold:1"
    },

    # 3.4 财阀 (Dao of Wealth)
    {
        "id": "ach_rich_1w", "category": "fortune", "name": "腰缠万贯", 
        "desc": "拥有灵石超过 10,000", 
        "condition_type": "currency", "condition_target": "money", "threshold": 10000,
        "reward_type": "title", "reward_value": "title_rich" # [多宝道人]
    },
    {
        "id": "ach_rich_100w", "category": "fortune", "name": "富可敌国", 
        "desc": "拥有灵石超过 1,000,000", 
        "condition_type": "currency", "condition_target": "money", "threshold": 1000000,
        "reward_type": "item", "reward_value": "metal_taiyi:1"
    },
    {
        "id": "ach_poor_0", "category": "fortune", "name": "身无分文", 
        "desc": "灵石少于 10 (需历史总获得 > 1000)", 
        "condition_type": "currency_low", "condition_target": "money", "threshold": 10,
        "reward_type": "item", "reward_value": "misc_broken_sword:1",
        "is_hidden": 1
    },
    {
        "id": "ach_spend_5k", "category": "fortune", "name": "挥金如土", 
        "desc": "在坊市累计消费超过 5,000 灵石", 
        "condition_type": "stat_total", "condition_target": "money_spent", "threshold": 5000,
        "reward_type": "item", "reward_value": "pill_beauty_face:1"
    },
    {
        "id": "ach_sell_100", "category": "fortune", "name": "陶朱公", 
        "desc": "累计出售物品 100 次", 
        "condition_type": "stat_total", "condition_target": "items_sold", "threshold": 100,
        "reward_type": "title", "reward_value": "title_merchant" # [精算师]
    },
    {
        "id": "ach_hoard_90", "category": "fortune", "name": "仓鼠精", 
        "desc": "背包占用率超过 90%", 
        "condition_type": "special", "condition_target": "inventory_fullness", "threshold": 90,
        "reward_type": "item", "reward_value": "soil_chaos:1"
    }
]

def init_achievements():
    print(f"Connecting to DB: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if table exists (handled by database.py but just in case)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id TEXT PRIMARY KEY,
            category TEXT,
            name TEXT,
            desc TEXT,
            condition_type TEXT,
            condition_target TEXT,
            threshold INTEGER,
            reward_type TEXT,
            reward_value TEXT,
            is_hidden INTEGER DEFAULT 0,
            status INTEGER DEFAULT 0,
            unlocked_at INTEGER
        )
    """)
    
    print(f"Injecting {len(ACHIEVEMENTS_DATA)} achievements...")
    
    count_new = 0
    count_update = 0
    
    for ach in ACHIEVEMENTS_DATA:
        # Upsert: if exists, update descriptions/rewards but keep status!
        # SQLite UPSERT syntax support > 3.24. 
        # Safe way: Select first.
        
        cursor.execute("SELECT status, unlocked_at FROM achievements WHERE id = ?", (ach['id'],))
        row = cursor.fetchone()
        
        if row:
            # Update meta info
            cursor.execute("""
                UPDATE achievements 
                SET category=?, name=?, desc=?, condition_type=?, condition_target=?, 
                    threshold=?, reward_type=?, reward_value=?, is_hidden=?
                WHERE id=?
            """, (
                ach['category'], ach['name'], ach['desc'], ach['condition_type'], ach['condition_target'],
                ach['threshold'], ach['reward_type'], ach['reward_value'], ach.get('is_hidden', 0),
                ach['id']
            ))
            count_update += 1
        else:
            # Insert new
            cursor.execute("""
                INSERT INTO achievements (
                    id, category, name, desc, condition_type, condition_target, 
                    threshold, reward_type, reward_value, is_hidden
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ach['id'], ach['category'], ach['name'], ach['desc'], ach['condition_type'], ach['condition_target'],
                ach['threshold'], ach['reward_type'], ach['reward_value'], ach.get('is_hidden', 0)
            ))
            count_new += 1
            
    conn.commit()
    conn.close()
    print(f"Done. New: {count_new}, Updated: {count_update}")

if __name__ == "__main__":
    init_achievements()

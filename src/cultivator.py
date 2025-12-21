import random
from src.logger import logger
from src.item_manager import ItemManager
from src.event_manager import EventManager

class Cultivator:
    LAYERS = [
        "炼气期", "筑基期", "金丹期", "元婴期", "化神期", "炼虚期", "合体期", "大乘期", "渡劫期"
    ]
    
    def __init__(self):
        self.exp = 0
        self.layer_index = 0
        self.money = 0 # 灵石
        self.inventory = {} # 物品栏 {id: count}
        self.events = [] # 事件日志
        
        # 核心属性
        self.mind = 0      # 心魔 (0-100)，越高修练越慢
        self.body = 10     # 体魄 (基础10)，影响渡劫成功率
        self.affection = 0 # 好感度 (0-100)，影响材料掉率
        
        # 坊市数据
        self.market_goods = [] # [{id, price, discount}]
        self.last_market_refresh = 0
        
        # 事件系统
        self.last_event_time = 0 
        self.event_interval = 300 # 300秒(5分钟)触发一次随机事件 (测试可改为30)
        
        # 初始化 ItemManager 和 EventManager
        self.item_manager = ItemManager()
        self.event_manager = EventManager()
        
        # 天赋系统
        self.talent_points = 0
        self.talents = {
            "exp": 0,  # 修炼天赋: +5% 经验获取
            "drop": 0  # 寻宝天赋: +5% 掉落概率
        }
        
    # ... (properties methods) ...

    def modify_stat(self, stat, value):
        if stat == "mind":
            self.mind = max(0, min(100, self.mind + value))
        elif stat == "body":
            self.body = max(1, self.body + value) # 体魄无上限
        elif stat == "affection":
            self.affection = max(0, min(100, self.affection + value))
        elif stat == "reset_talent":
            self.reset_talents()
            
    def reset_talents(self):
        total = sum(self.talents.values())
        self.talents["exp"] = 0
        self.talents["drop"] = 0
        self.talent_points += total
        logger.info(f"洗髓成功! 返还 {total} 天赋点")

    def upgrade_talent(self, talent_type):
        if self.talent_points > 0 and talent_type in self.talents:
            self.talents[talent_type] += 1
            self.talent_points -= 1
            return True
        return False

    def refresh_market(self):
        """刷新坊市商品 (每天一次 or 手动)"""
        import time
        self.last_market_refresh = time.time()
        self.market_goods = []
        
        # 随机生成 6 个商品
        # 逻辑：3个材料，2个消耗品，1个珍稀(低概率)
        # 简单实现：从当前 Tier 和 上一 Tier 随机抽取
        current_tier = 1 if self.layer_index == 0 else 2
        
        for _ in range(6):
            # 随机决定类型
            roll = random.random()
            if roll < 0.6: # 60% 材料
                item_id = self.item_manager.get_random_material(current_tier)
            else: # 40% 丹药
                candidates = self.item_manager.tier_lists[current_tier]["pills"]
                item_id = random.choice(candidates) if candidates else None
                
            if item_id:
                info = self.item_manager.get_item(item_id)
                base_price = info.get("price", 100)
                
                # 随机折扣 (0.8 ~ 1.25)
                discount = round(random.uniform(0.8, 1.2), 2)
                final_price = int(base_price * discount)
                
                self.market_goods.append({
                    "id": item_id,
                    "price": final_price,
                    "discount": discount
                })
        
        logger.info("坊市商品已刷新")

    def check_daily_refresh(self):
        """检查是否需要每日自动刷新"""
        import time
        # 简单判断: 超过24小时刷新? 或者每天0点?
        # 这里用简单的时间间隔: 8小时刷新一次
        if time.time() - self.last_market_refresh > 8 * 3600:
            self.refresh_market()

    # ... (existing methods) ...

    def save_data(self, filepath):
        import json
        import time
        data = {
            "exp": self.exp,
            "layer_index": self.layer_index,
            "money": self.money,
            "inventory": self.inventory,
            "last_save_time": time.time(),
            "market_goods": self.market_goods,
            "last_market_refresh": self.last_market_refresh
        }
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f)
            logger.info("数据已保存")
        except Exception as e:
            logger.error(f"保存失败: {e}")

    def load_data(self, filepath):
        import json
        import os
        if not os.path.exists(filepath):
            # 新存档，初始化坊市
            self.refresh_market()
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.exp = data.get("exp", 0)
                self.layer_index = data.get("layer_index", 0)
                self.money = data.get("money", 0)
                self.inventory = data.get("inventory", {})
                self.market_goods = data.get("market_goods", [])
                self.last_market_refresh = data.get("last_market_refresh", 0)
                
                stats = data.get("stats", {})
                self.mind = stats.get("mind", 0)
                self.body = stats.get("body", 10)
                self.affection = stats.get("affection", 0)
                
                # 结算离线
                last_time = data.get("last_save_time", 0)
                if last_time > 0:
                    self.calculate_offline_progress(last_time)
            
            # 检查刷新
            self.check_daily_refresh()
            if not self.market_goods:
                self.refresh_market()
                
            logger.info("数据已加载")
        except Exception as e:
            logger.error(f"加载失败: {e}")

    @property
    def current_layer(self):
        if self.layer_index < len(self.LAYERS):
            return self.LAYERS[self.layer_index]
        return "飞升仙界"

    @property
    def max_exp(self):
        # 简单的指数级经验曲线
        return 100 * (2 ** self.layer_index)

    def gain_exp(self, amount):
        self.exp += amount
        
        # 达到瓶颈
        if self.exp >= self.max_exp:
            self.exp = self.max_exp
            # 不自动升级，需要手动渡劫
        
        return False # 移除 auto level up 的返回值意义，或者是 keep signature

    def can_breakthrough(self):
        return self.exp >= self.max_exp and self.layer_index < len(self.LAYERS) - 1

    def attempt_breakthrough(self, base_success_rate=None):
        """
        尝试渡劫/突破
        :param base_success_rate: 如果提供 (0.0-1.0), 则使用此固定基础概率(丹药效果)，否则根据属性计算
        Return: (success: bool, message: str)
        """
        if not self.can_breakthrough():
            # 即使是有丹药，修为不够也不能突破 (除非是特殊的挂开药)
            return False, "修为尚未圆满，强行突破必死无疑。"
            
        import random
        
        if base_success_rate is not None:
             # 丹药突破: 固定概率 + 体魄/心魔修正(稍微小一点影响)
             # 既然是丹药，我们假设它主要看药效，但属性依然有微调
             success_rate = base_success_rate + (self.body * 0.005) - (self.mind * 0.005)
             method_str = "丹药辅助"
        else:
             # 自然突破
             # 基础成功率 50%
             # 体魄加成: 每点 +1% 
             # 心魔惩罚: 每点 -0.5%
             success_rate = 0.5 + (self.body * 0.01) - (self.mind * 0.005)
             method_str = "顺其自然"
             
        success_rate = max(0.01, min(0.99, success_rate)) # 限制范围
        
        roll = random.random()
        logger.info(f"渡劫判定({method_str}): Roll {roll:.2f} < Rate {success_rate:.2f}")
        
        if roll < success_rate:
            # 成功
            self.exp = 0 
            self.layer_index += 1
            
            # 成功奖励: 属性提升，清除少量心魔
            self.body += 2
            self.mind = max(0, self.mind - 20)
            self.talent_points += 1 # 获得天赋点
            
            msg = f"雷劫洗礼，金光护体！\n晋升【{self.current_layer}】\n体魄+2，天赋点+1"
            self.events.append(msg)
            return True, msg
        else:
            # 失败惩罚
            # ... (unchanged) ...
            loss = int(self.max_exp * 0.3)
            self.exp -= loss
            self.body = max(0, self.body - 1)
            self.mind = min(100, self.mind + 10)
            
            msg = f"渡劫失败！天雷滚滚，肉身受损。\n修为-{loss}，体魄-1，心魔+10"
            self.events.append(msg)
            return False, msg

    def gain_item(self, item_id, count=1):
        if item_id in self.inventory:
            self.inventory[item_id] += count
        else:
            self.inventory[item_id] = count
            
        # item_name = self.item_manager.get_item_name(item_id)
        # self.events.append(f"获得: {item_name} x{count}")
        # 暂时屏蔽获得物品的公共日志，避免刷屏？
        pass

    def update(self, kb_apm, mouse_apm):
        """
        根据 键鼠APM 更新状态并返回获得的收益描述
        """
        gain_msg = ""
        current_state_code = 0 
        
        # Mapping Tier
        current_tier = 1 if self.layer_index == 0 else 2 
        
        # 0. 心魔与天赋判定
        # 天赋加成
        talent_exp_bonus = 1.0 + (self.talents.get("exp", 0) * 0.05)
        talent_drop_bonus = self.talents.get("drop", 0) * 0.05
        
        # 心魔惩罚: >50 开始衰减 exp 获取, 100 时无法获取 EXP
        exp_efficiency = 1.0 * talent_exp_bonus
        if self.mind > 50:
            penalty = (self.mind - 50) * 0.02 # 每点 -2%
            exp_efficiency = max(0, exp_efficiency - penalty)
            if random.random() < 0.05: # 偶尔提示
                 gain_msg = "心神不宁..."
        
        # 1. 判定状态
        if kb_apm < 30 and mouse_apm < 30:
            # IDLE
            current_state_code = 0 
            base_exp = 1 
            gain_msg = f"+{base_exp} 修为"
            if talent_exp_bonus > 1.0: gain_msg += " (天赋↑)"
            
        elif kb_apm >= 30 and mouse_apm < 30:
            # WORK: 键盘历练
            current_state_code = 2 
            base_exp = 5
            
            # 好感度加成掉落率
            drop_bonus = (self.affection * 0.002) + talent_drop_bonus # max +20% from aff, +5% * talent
            
            if random.random() < (0.05 + drop_bonus):
                drop_id = self.item_manager.get_random_material(current_tier)
                if drop_id:
                    self.gain_item(drop_id)
                    name = self.item_manager.get_item_name(drop_id)
                    gain_msg = f"探险发现: {name}!"
                
            if not gain_msg:
                gain_msg = "+5 修为 (历练中)"

        elif kb_apm < 30 and mouse_apm >= 30:
            # READ: 悟道
            current_state_code = 3 
            base_exp = 8 
            gain_msg = "+8 修为 (悟道中)"
            
            if random.random() < 0.02:
                base_exp += 20
                gain_msg = "顿悟! +28 修为"
                # 顿悟减少心魔
                self.mind = max(0, self.mind - 5)
                
        else:
            # COMBAT: 斗法
            current_state_code = 1 
            base_exp = 15 
            gain_msg = "火力全开! +15 修为"
            
            # 战斗增加少量心魔风险
            if random.random() < 0.01:
                self.mind = min(100, self.mind + 1)
                gain_msg = "杀气过重! 心魔+1"
        
        # 应用心魔惩罚
        final_exp = int(base_exp * exp_efficiency)
        if final_exp == 0 and base_exp > 0:
             gain_msg = "心魔缠身，修为停滞！"
             
        self.gain_exp(final_exp)
        
        # --- 随机事件系统 ---
        self.tick_counter = getattr(self, 'tick_counter', 0) + 1
        if self.tick_counter >= self.event_interval:
            self.tick_counter = 0
            event = self.event_manager.get_random_event(self)
            if event:
                if event['type'] == 'random':
                    logger.info(f"触发随机事件: {event['text']}")
                    effect_texts = self.event_manager.apply_event_effect(self, event.get('effects', {}))
                    
                    full_msg = f"【机缘】{event['text']}"
                    if effect_texts:
                         full_msg += f"\n> {' '.join(effect_texts)}"
                    self.events.append(full_msg)
                else:
                    logger.info(f"触发特殊事件(未实装UI): {event['text']}")

            
        return gain_msg, current_state_code
    
    def calculate_offline_progress(self, last_timestamp):
        import time
        current_time = time.time()
        # 即使数据没有 timestamp，也要处理
        if not last_timestamp:
            return 
            
        diff = int(current_time - last_timestamp)
        if diff > 60: # 离线超过1分钟才结算
            # 离线默认按打坐计算，但收益减半 (2.5 exp/s)
            exp_gain = int(diff * 2.5)
            self.gain_exp(exp_gain)
            self.events.append(f"闭关结束，离线 {diff // 60} 分钟，获得 {exp_gain} 修为")
            
    def get_random_dialogue(self):
        dialogues = [
            "道可道，非常道...",
            "别摸了，贫道要走火入魔了！",
            "今日宜修炼，忌摸鱼。",
            "我感觉我要突破了！",
            "这位道友，我看你骨骼精奇...",
            "还不快去写代码？",
            "只有充钱才能变得更强（误",
            "修仙本是逆天而行...",
            "灵气...这里的灵气太稀薄了。",
        ]
        return random.choice(dialogues)

    def save_data(self, filepath):
        import json
        import time
        data = {
            "exp": self.exp,
            "layer_index": self.layer_index,
            "money": self.money,
            "inventory": self.inventory,
            "last_save_time": time.time(),
            "market_goods": self.market_goods,
            "last_market_refresh": self.last_market_refresh,
            "stats": {
                "mind": self.mind,
                "body": self.body,
                "affection": self.affection
            },
            "talents": self.talents,
            "talent_points": self.talent_points
        }
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f)
            logger.info("数据已保存")
        except Exception as e:
            logger.error(f"保存失败: {e}")

    def load_data(self, filepath):
        import json
        import os
        if not os.path.exists(filepath):
            # 新存档，初始化坊市
            self.refresh_market()
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.exp = data.get("exp", 0)
                self.layer_index = data.get("layer_index", 0)
                self.money = data.get("money", 0)
                self.inventory = data.get("inventory", {})
                self.market_goods = data.get("market_goods", [])
                self.last_market_refresh = data.get("last_market_refresh", 0)
                
                stats = data.get("stats", {})
                self.mind = stats.get("mind", 0)
                self.body = stats.get("body", 10)
                self.affection = stats.get("affection", 0)
                
                self.talents = data.get("talents", {"exp": 0, "drop": 0})
                self.talent_points = data.get("talent_points", 0)
                
                # 结算离线
                last_time = data.get("last_save_time", 0)
                if last_time > 0:
                    self.calculate_offline_progress(last_time)
            
            # 检查刷新
            self.check_daily_refresh()
            if not self.market_goods:
                self.refresh_market()
                    
            logger.info("数据已加载")
        except Exception as e:
            logger.error(f"加载失败: {e}")

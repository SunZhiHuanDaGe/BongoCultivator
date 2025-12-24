import json
import os
import random
from src.logger import logger

class EventManager:
    def __init__(self, data_path=None):
        from src.utils.path_helper import get_resource_path
        
        if data_path is None:
            # 默认路径
            data_path = get_resource_path(os.path.join('src', 'data', 'events.json'))
            
        self.events = []
        self.load_events(data_path)
        
    def load_events(self, path):
        if not os.path.exists(path):
            logger.error(f"事件数据文件未找到: {path}")
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.events = json.load(f)
            logger.info(f"成功加载 {len(self.events)} 个随机事件")
        except Exception as e:
            logger.error(f"加载事件数据失败: {e}")

    def get_random_event(self, cultivator):
        """
        根据修炼者当前状态，随机抽取一个符合条件的事件
        """
        valid_events = []
        total_weight = 0
        
        for event in self.events:
            # 1. 检查条件
            if self._check_conditions(event, cultivator):
                valid_events.append(event)
                total_weight += event.get('weight', 10)
                
        if not valid_events:
            return None
            
        # 2. 权重随机
        r = random.uniform(0, total_weight)
        current_weight = 0
        for event in valid_events:
            current_weight += event.get('weight', 10)
            if r <= current_weight:
                return event
                
        return valid_events[0]
    
    def _check_conditions(self, event, cultivator) -> bool:
        conditions = event.get('conditions', {})
        
        # 境界检查
        if 'min_layer' in conditions and cultivator.layer_index < conditions['min_layer']:
            return False
            
        # 灵石检查
        if 'min_money' in conditions and cultivator.money < conditions['min_money']:
            return False
            
        # 属性检查
        if 'min_mind' in conditions and cultivator.mind < conditions['min_mind']:
            return False
        if 'max_mind' in conditions and cultivator.mind > conditions['max_mind']:
            return False
            
        return True

    def apply_event_effect(self, cultivator, effect):
        """
        应用事件效果 (直接修改 cultivator 属性)
        返回效果描述文本
        """
        result_texts = []
        
        # 文本描述
        if 'text' in effect:
            result_texts.append(effect['text'])
            
        # 资源变动
        if 'money' in effect:
            val_range = effect['money']
            val = random.randint(val_range[0], val_range[1])
            cultivator.money += val
            result_texts.append(f"灵石 {'+' if val>0 else ''}{val}")
            
        if 'exp' in effect:
            val_range = effect['exp']
            val = random.randint(val_range[0], val_range[1])
            cultivator.exp += val
            result_texts.append(f"修为 {'+' if val>0 else ''}{val}")
            
        # 属性变动
        if 'mind' in effect:
            val_range = effect['mind']
            val = random.randint(val_range[0], val_range[1])
            cultivator.mind += val
            # 边界检查由 Cultivator 属性负责，或者在这里手动 clamp
            cultivator.mind = max(0, min(100, cultivator.mind))
            result_texts.append(f"心魔 {'+' if val>0 else ''}{val}")
            
        if 'body' in effect:
            val_range = effect['body']
            val = random.randint(val_range[0], val_range[1])
            cultivator.body += val
            cultivator.body = max(0, min(100, cultivator.body))
            result_texts.append(f"淬体 {'+' if val>0 else ''}{val}")

        # 物品获取
        if 'items' in effect:
            items = effect['items']
            for item_id, count in items.items():
                cultivator.gain_item(item_id, count)
                # gain_item 内部没有返回物品名，这里最好通过 ItemManager 获取一下名字用于显示
                # 暂时略过名字获取，直接显示
                result_texts.append(f"获得物品 [{item_id}] x{count}")
                
        return result_texts

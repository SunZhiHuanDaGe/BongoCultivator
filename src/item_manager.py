import json
import os
import random
from src.logger import logger

class ItemManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ItemManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        
        self.items_data = {}
        self.flat_items = {} # id -> item_info mapping for quick lookup
        self.tier_lists = {
            1: {"materials": [], "pills": []},
            2: {"materials": [], "pills": []}
        }
        
        self.load_items()
        self.initialized = True

    def load_items(self):
        try:
            # Locate items.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, 'data', 'items.json')
            
            with open(json_path, 'r', encoding='utf-8') as f:
                self.items_data = json.load(f)
                
            self._process_data()
            logger.info(f"成功加载物品数据库，共 {len(self.flat_items)} 种物品。")
        except Exception as e:
            logger.error(f"加载物品数据库失败: {e}")

    def _process_data(self):
        # Process Tier 1
        t1 = self.items_data.get("tier_1", {})
        self._add_to_cache(1, t1.get("materials", []), "materials")
        self._add_to_cache(1, t1.get("pills", []), "pills")

        # Process Tier 2
        t2 = self.items_data.get("tier_2", {})
        self._add_to_cache(2, t2.get("materials", []), "materials")
        self._add_to_cache(2, t2.get("pills", []), "pills")

    def _add_to_cache(self, tier, item_list, category):
        for item in item_list:
            item_id = item.get("id")
            if item_id:
                self.flat_items[item_id] = item
                self.tier_lists[tier][category].append(item_id)

    def get_item(self, item_id):
        return self.flat_items.get(item_id)

    def get_random_material(self, tier):
        """Randomly return a material ID from the specified tier"""
        candidates = self.tier_lists.get(tier, {}).get("materials", [])
        if candidates:
            return random.choice(candidates)
        return None

    def get_item_name(self, item_id):
        info = self.flat_items.get(item_id)
        return info["name"] if info else item_id

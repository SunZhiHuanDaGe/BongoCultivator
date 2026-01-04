
import sys
import os
import json
from sqlmodel import Session, select

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import db_manager
from src.models import ItemDefinition

def update_effects():
    # Define the mapping of item_id -> new effect dict
    updates = {
        # T0
        "pill_detox": {"stat_body": 1},
        "pill_speed": {"mind_heal": 5},
        "pill_waste": {"mind_heal": -5},
        "water_rootless": {"mind_heal": 5},
        # T1
        "milk_earth": {"stat_body": 2},
        "pill_night": {"affection": 2},
        # T2
        "pill_beauty": {"affection": 5},
        "pill_burn_blood": {"exp_gain": 0.05, "stat_body": -2},
        "pill_luck_small": {"affection": 10},
        # T3
        "pill_clone": {"exp_gain": 0.10},
        "charm_teleport": {"exp": 1000},
        "water_ghost": {"mind_heal": -10, "stat_body": 3},
        # T4
        "pill_break_rule": {"mind_heal": 30},
        "water_heavy": {"stat_body": 5},
        # T5
        "pill_dimension": {"affection": 15},
        "pill_rebirth_body": {"stat_body": 20, "mind_heal": 20},
        # T6
        "pill_nine_turn": {"stat_body": 10, "mind_heal": 50, "exp_gain": 0.1},
        "water_creation": {"stat_body": 10, "affection": 10},
        # T7
        "pill_immortality": {"stat_body": 50},
        "pill_regret": {"mind_heal": 100},
        # T8
        "water_thunder": {"stat_body": 20, "exp_gain": 0.20},
        "pill_avoid_thunder": {"breakthrough_chance": 0.3},
        "pill_ascension": {"exp_gain": 0.50}
    }

    print(f"准备更新 {len(updates)} 个物品的效果...")

    updated_count = 0
    with db_manager.get_session() as session:
        for item_id, new_effect in updates.items():
            item = session.get(ItemDefinition, item_id)
            if item:
                # Merge with existing? Or overwrite? 
                # Proposal: Overwrite to ensure clean state based on documentation.
                # User wants "every pill to have effect", so we define everything.
                
                # Check if it has existing critical effects (like breakthrough chance for some items?)
                # pill_avoid_thunder is new.
                
                old_json = item.effect_json
                item.effect_json = json.dumps(new_effect)
                session.add(item)
                updated_count += 1
                print(f"Updated {item.name} ({item_id}): {new_effect}")
            else:
                print(f"Warning: Item {item_id} not found in DB.")
        
        session.commit()
    
    print(f"更新完成，共更新 {updated_count} 个物品。")

if __name__ == "__main__":
    update_effects()

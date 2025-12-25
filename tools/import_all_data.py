import json
import sqlite3
import os
import sys

# Define file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_V1_PATH = os.path.join(BASE_DIR, "src", "data", "items.json")
ITEMS_V2_PATH = os.path.join(BASE_DIR, "src", "data", "items_v2.json")
EVENTS_PATH = os.path.join(BASE_DIR, "src", "data", "events.json")
DB_PATH = os.path.join(BASE_DIR, "user_data.db")

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return {}

def main():
    print("Starting All Data Import Tool...")
    
    # --- 1. Load Data Sources ---
    v1_items = load_json(ITEMS_V1_PATH)
    v2_items = load_json(ITEMS_V2_PATH)
    events_data = load_json(EVENTS_PATH)
    
    # --- 2. Process Items & Recipes ---
    combined_items = {}
    
    def process_tier_data(tier_data):
        if not tier_data: return
        for category in ["materials", "pills", "equipments", "books"]:
            if category in tier_data:
                for item in tier_data[category]:
                    item_id = item.get("id")
                    if not item_id: continue
                    
                    effect_val = json.dumps(item.get("effect", {})) if isinstance(item.get("effect"), dict) else item.get("effect", "{}")
                    recipe_val = json.dumps(item.get("recipe", {})) if isinstance(item.get("recipe"), dict) else item.get("recipe", "{}")
                    
                    combined_items[item_id] = {
                        "id": item_id,
                        "name": item.get("name"),
                        "type": item.get("type"),
                        "tier": item.get("tier"),
                        "price": item.get("price"),
                        "description": item.get("desc"),
                        "effect": effect_val,
                        "recipe": recipe_val
                    }

    # Load V2 first, then V1 overrides
    print("Processing items_v2.json...")
    for data in v2_items.values(): process_tier_data(data)
    print("Processing items.json...")
    for data in v1_items.values(): process_tier_data(data)
    
    print(f"Total Unique Items: {len(combined_items)}")

    # --- 3. SQLite Sync ---
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # --- A. Items ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_definitions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT,
                tier INTEGER DEFAULT 0,
                description TEXT,
                price INTEGER DEFAULT 0,
                effect_json TEXT
            )
        """)
        cursor.execute("DELETE FROM item_definitions")
        
        count_items = 0
        for item in combined_items.values():
            cursor.execute("""
                INSERT INTO item_definitions (id, name, type, tier, description, price, effect_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item["id"], item["name"], item["type"], item["tier"], item["description"], item["price"], item["effect"]))
            count_items += 1
            
        # --- B. Recipes ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_item_id TEXT,
                ingredients_json TEXT,
                craft_time INTEGER DEFAULT 5,
                success_rate REAL DEFAULT 1.0,
                FOREIGN KEY(result_item_id) REFERENCES item_definitions(id)
            )
        """)
        cursor.execute("DELETE FROM recipes")
        
        count_recipes = 0
        for item in combined_items.values():
            recipe_str = item["recipe"]
            if recipe_str and recipe_str != "{}":
                cursor.execute("""
                    INSERT INTO recipes (result_item_id, ingredients_json, craft_time, success_rate)
                    VALUES (?, ?, ?, ?)
                """, (item["id"], recipe_str, 5, 1.0))
                count_recipes += 1

        # --- C. Events ---
        print("Processing events.json...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_definitions (
                id TEXT PRIMARY KEY,
                type TEXT,
                weight INTEGER,
                data_json TEXT
            )
        """)
        cursor.execute("DELETE FROM event_definitions")
        
        count_events = 0
        if isinstance(events_data, list):
            for event in events_data:
                evt_id = event.get("id")
                evt_type = event.get("type", "random")
                evt_weight = event.get("weight", 10)
                # Store the FULL event object as json
                evt_json = json.dumps(event)
                
                cursor.execute("""
                    INSERT INTO event_definitions (id, type, weight, data_json)
                    VALUES (?, ?, ?, ?)
                """, (evt_id, evt_type, evt_weight, evt_json))
                count_events += 1
        
        conn.commit()
        print("="*40)
        print(f"DATABASE UPDATE SUCCESSFUL")
        print(f"Items Imported:   {count_items}")
        print(f"Recipes Imported: {count_recipes}")
        print(f"Events Imported:  {count_events}")
        print("="*40)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn: conn.close()
        
if __name__ == "__main__":
    main()

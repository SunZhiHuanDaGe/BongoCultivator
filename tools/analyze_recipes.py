import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user_data.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Get all materials
    cursor.execute("SELECT id, name, tier FROM item_definitions WHERE type='material'")
    materials = {row['id']: dict(row) for row in cursor.fetchall()}
    
    # 2. Get all recipes
    cursor.execute("SELECT * FROM recipes")
    recipes = [dict(row) for row in cursor.fetchall()]

    # 3. Analyze usage
    used_materials = set()
    for r in recipes:
        ingredients = json.loads(r['ingredients_json'])
        for mat_id in ingredients.keys():
            used_materials.add(mat_id)

    unused = [m_id for m_id in materials if m_id not in used_materials]
    
    print(f"Total Materials: {len(materials)}")
    print(f"Used Materials: {len(used_materials)}")
    print(f"Unused Materials ({len(unused)}):")
    for u in unused:
        mat = materials[u]
        print(f" - [{u}] {mat['name']} (Tier {mat['tier']})")

    # 4. Fix: Generate Recycling Recipes for Unused Materials
    # Logic: 3x Material -> 1x Spirit Shard (or equivalent currency item, or just money?)
    # We don't have a "Spirit Shard". Let's use "pill_qi" (Tier 1 Exp Pill) or just a generic trade.
    # Actually, in Plan 15, we said: "Universal recycling recipes: 3x Low Mat -> 1x Spirit Liquid/Shard".
    # Let's check if we have a generic "Spirit Liquid" or something.
    # If not, maybe create one? Or just map to existing low-tier consumable like 'rice_spirit' (Tier 1 Consumable).
    
    # Let's create proper recipes for them:
    # - If Tier 1 Unused: 3x Mat -> 1x rice_spirit (Price 3)
    # - If Tier 2 Unused: 3x Mat -> 1x pill_qi (Price 50) - maybe too high? 
    # Let's just create a "Recycle" mechanic where they can simple craft "Spirit Sand" which sells for money?
    # Or better: Just ensure they are used in SOME potion.
    
    # Auto-generater strategy:
    # Pair unused materials with existing potions of same tier.
    # E.g. Unused 'iron_waste' -> added as alternative ingredient to 'pill_strengh'?
    # Simpler: Create "Essence Extraction" recipes.
    # 5x [Unused Mat] -> 1x [Stat Pill of same Tier] (low chance?)
    
    # For now, let's just List them so I (the AI) can verify what needs to be done.
    
    conn.close()

if __name__ == "__main__":
    main()

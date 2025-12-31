# Plan 23: 数据同步与版本控制 (Data Sync & Version Control)

## 问题背景 (Problem Context)
用户担心当游戏更新（代码更新）时，本地数据库 (`user_data.db`) 中的静态数据（物品、事件、配方）会过时，无法与新程序兼容。
目前 `DataLoader.load_initial_data()` 逻辑似乎只在数据库为空时才执行，或者手动触发。

## 目标 (Goals)
1.  **自动同步**: 每次启动游戏时，自动检查代码中的静态数据版本（JSON 文件）是否比数据库中的新。
2.  **增量更新**: 如果有更新，自动将新物品、新事件写入数据库，同时**保留用户的存档数据**（inventory, player_status）。

## 解决方案 (Solution)

### 1. 引入版本号机制 (Data Versioning)
在 `user_data.db` 中增加一个 `system_metadata` 表，存储当前数据的版本号。
在 `src/services/data_loader.py` 中定义代码当前的 `DATA_VERSION`。

### 2. 启动检查流程
每次 `main.py` 启动时：
1.  读取 DB 中的 `data_version`。
2.  读取代码中的 `DATA_VERSION`。
3.  如果 `DB_VERSION < CODE_VERSION`：
    - 执行 `DataLoader.update_static_data()`。
    - 更新物品定义、配方、事件（由于这些是静态数据，可以直接覆盖/插入 `INSERT OR REPLACE`）。
    - 更新 DB 中的版本号。

## 实施步骤 (Implementation Steps)

### 步骤 1: 修改 `src/database.py`
创建 `system_metadata` 表。

```python
# src/database.py
def init_db(self):
    # ... existing tables ...
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
```

### 步骤 2: 修改 `src/services/data_loader.py`
增加版本号常量和更新逻辑。

```python
DATA_VERSION = "1.2" # 每次修改 JSON 后手动增加这个值

def check_data_version():
    # Load version from DB
    # Load version from Code
    # If update needed -> load_initial_data(force_update=True)
    pass
```

### 步骤 3: 优化 `load_initial_data`
使其支持**非破坏性更新**。
- `player_inventory` 和 `player_status` **绝对不能** 动。
- `item_definitions`, `recipes`, `event_definitions` 可以被覆盖（因为它们是静态配置）。
- 注意：如果旧物品被删除，是否要从用户背包删除？通常为了兼容性，我们只做**新增**和**修改**，不物理删除旧定义（或者保留定义但在背包中标记过期）。目前的策略是 `INSERT OR REPLACE`，这很好。

### 步骤 4: 在 `main.py` 调用
在 `check_and_migrate_data()` (Plan 22) 之后，调用 `check_data_update()`。

## 验证计划
1.  手动修改 `items_v2.json`，增加一个测试物品。
2.  修改 `DATA_VERSION`。
3.  启动游戏。
4.  检查日志是否提示“正在更新数据...”。
5.  检查新物品是否出现在数据库中。

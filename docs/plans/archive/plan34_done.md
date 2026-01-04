---
description: Fix untranslated 'pill_waste' item by adding its definition to the game data.
---

# Plan 34: Fix Untranslated Item ("pill_waste")

## 1. 问题分析 (Problem Analysis)
用户反馈在 UI 中（如下拉列表）看到了 `pill_waste` 的英文显示，而不是中文名称。
经检查代码，发现在 `src/pet_window.py` 的炼丹逻辑中，当炼丹失败时会给予玩家 `pill_waste` 物品：
```python
self.cultivator.gain_item("pill_waste", 1)
```
然而，`pill_waste` 在 `src/data/items_v2.json` 和数据库中均未定义，导致系统回退显示物品 ID。

## 2. 解决方案 (Solution)
我们需要在 `src/data/items_v2.json` 中添加 `pill_waste` 的定义，并通过 `src/services/data_loader.py` 触发数据库更新。

### 2.1 添加物品定义
在 `src/data/items_v2.json` 的 `tier_0` -> `junk` (或 `pills`) 分类下添加：
```json
{
    "id": "pill_waste",
    "name": "废丹",
    "type": "junk",
    "tier": 0,
    "price": 1,
    "desc": "炼丹失败的产物，散发着焦糊味，毫无药用价值。",
    "effect": {},
    "recipe": {}
}
```

### 2.2 触发数据同步
修改 `src/services/data_loader.py` 中的 `DATA_VERSION`，将其从当前版本 (如 "003") 增加到新版本 (如 "004")。这将迫使应用在下次启动时重新加载 JSON 数据到 SQLite 数据库。

## 3. 执行步骤 (Execution Steps)
1.  **编辑 `src/data/items_v2.json`**: 添加 `pill_waste` 定义。
2.  **编辑 `src/services/data_loader.py`**: 增加版本号。
3.  **验证**: (无法直接运行验证，但可以通过检查代码确认逻辑正确性)。

## 4. 后续 (Follow-up)
- 确保所有新添加的物品都有对应的定义。
- 建议未来在 `gain_item` 时增加检查，如果是未知物品 ID 则打印警告。

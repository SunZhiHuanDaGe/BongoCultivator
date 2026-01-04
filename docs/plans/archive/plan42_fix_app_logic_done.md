# Plan 42: 修复资源扣除逻辑 (Fix Resource Consumption Logic)

## 🐛 问题描述 (Issue)
用户反馈炼丹时可以重复点击或在材料不足时继续炼制，导致材料数量变为负数。这通常是因为在扣除材料前没有进行原子性的检查（Atomic Check），或者在扣除过程中部分扣除失败导致数据不一致。

同样的问题可能存在于坊市购买（灵石扣除）和出售（物品扣除）逻辑中。

## 🎯 目标 (Goals)
1.  **集中管理资源扣除**: 在 `Cultivator` 类中实现统一的、安全的资源消耗方法。
2.  **原子性操作**: 确保“检查”和“扣除”是不可分割的，或者在扣除前进行全量检查。如果材料不足，则**一个都不扣**。
3.  **修复 UI 调用**: 更新 `AlchemyWindow` 和 `MarketWindow` 调用新的安全方法。

## 🛠️ 实施方案 (Implementation Details)

### 1. 修改 `src/cultivator.py`
添加以下安全方法：
- `def has_items(self, items_dict: dict) -> bool`: 检查是否拥有指定数量的所有物品。
- `def consume_items(self, items_dict: dict) -> bool`: 
    - 先调用 `has_items` 检查所有材料。
    - 如果满足，则执行扣除，并清理数量为 0 的条目。
    - 如果不满足，返回 `False` 且不扣除任何物品。
- `def consume_money(self, amount: int) -> bool`: 安全扣除灵石。
- `def sell_item(self, item_id: str, count: int, unit_price: int) -> int`: 安全出售物品并增加灵石，返回获得的总金额。

### 2. 修改 `src/alchemy_window.py`
- 更新 `start_crafting` 方法：
    - 使用 `self.cultivator.consume_items(recipe)` 替代原有的直接遍历扣除逻辑。
    - 只有当返回 `True` 时，才触发 `self.pet_window.start_alchemy_task` 和关闭窗口。
    - 如果返回 `False`，提示“材料不足”或刷新界面。

### 3. 修改 `src/market_window.py`
- 更新 `buy_item` 使用 `consume_money`。
- 更新 `sell_item_one` 和 `sell_item_all` 使用 `sell_item`。

## 📋 执行步骤 (Execution Steps)
- [x] **创建验证脚本 `tools/verify_plan42.py`**:
    - 模拟 `Cultivator` 对象和库存。
    - 测试用例 1: 材料充足，消耗成功，库存减少。
    - 测试用例 2: 材料部分不足，消耗失败，库存**完全不变**（由原本的逻辑可能导致的负数或部分扣除问题）。
    - 测试用例 3: 灵石不足购买失败。
- [x] **重构 `src/cultivator.py`**: 实现上述安全方法。
- [x] **重构 `src/alchemy_window.py`**: 应用 `consume_items`。
- [x] **重构 `src/market_window.py`**: 应用 `consume_money` 和 `sell_item`。
- [x] **运行验证**: 执行脚本确保护盾逻辑生效。

## 📝 验收标准 (Acceptance Criteria)
1.  验证脚本通过所有测试用例。
2.  在游戏中，当材料刚好足够时可以炼丹；当材料不足时（例如狂点导致第一次扣除后不足），后续操作无效且不扣除材料，不产生负数。

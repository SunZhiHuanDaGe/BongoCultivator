# Plan 43: 修复炼丹按钮状态与UI同步 (Fix Alchemy Button & UI Sync)

## 🐛 问题描述 (Issue)
用户反馈：炼丹结束后，虽然材料已消耗（符合 Plan 42 的修正），但“炼丹按钮”仍然处于可点击状态，导致可以重复尝试（虽然可能因为 Plan 42 的护盾而失败，通过报错或无反应，但 UI 状态不正确）。

这表明 UI 的刷新机制（`refresh_recipes` 和 `show_recipe_detail`）可能没有正确反映最新的库存状态，或者窗口重新打开时的初始化逻辑有遗漏。

## 🎯 目标 (Goals)
1.  **防止重复提交**: 点击“开始炼制”后立即禁用按钮，防止连点。
2.  **强制 UI 刷新**: 确保每次窗口显示 (`showEvent`) 时，强制重新计算当前选定配方的可用性。
3.  **增加调试日志**: 追踪库存数量变化的读取情况，确认是数据问题还是 UI 问题。

## 🛠️ 实施方案 (Implementation Details)

### 1. 修改 `src/alchemy_window.py`
- **`start_crafting`**:
    - 进入方法首行立即 `self.craft_btn.setEnabled(False)`。
    - 添加日志：打印当前库存和配方需求。
- **`show_recipe_detail`**:
    - 添加日志：打印检查过程中的 `has_count` 和 `req_count`。
- **`showEvent`**:
    - 现有代码已调用 `refresh_recipes`。
    - 需确保如果 list 中有先前选中的 item，重新触发一次 `show_recipe_detail`（或者清除选中状态让用户重新选）。如果保留选中状态但数据过时，会导致详情页显示旧数据。
    - **改进**: 在 `refresh_recipes` 后，如果 `self.current_recipe_id` 存在，尝试重新选中对应的 item 并更新详情。

## 📋 执行步骤 (Execution Steps)
- [x] **修改 `src/alchemy_window.py`**:
    - 在 `start_crafting` 中添加防抖（Disable button）。
    - 优化 `refresh_recipes` 逻辑，确保 UI 状态（颜色/文本）与最新库存绝对同步。
    - 在 `show_recipe_detail` 中增加对 `current_recipe_id` 的实时库存检查日志。
- [x] **验证**:
    - 启动游戏，打开炼丹窗口。
    - 记录当前材料数量。
    - 点击炼制，观察窗口关闭和按钮状态。
    - 等待炼制完成（或直接关闭窗口），再次打开。
    - 检查按钮是否正确置灰（如果材料已耗尽）。

## 📝 验收标准 (Acceptance Criteria)
1.  炼丹时，点击按钮后按钮立刻变灰。
2.  材料不足时，重新打开窗口，对应的丹方应显示为灰色（[材料不足]），且详情页按钮不可点击。

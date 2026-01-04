# Plan 41: 修复日志窗口报错 (Fix Log Window NameError)

## 🐛 问题描述 (Issue)
用户反馈点击“修仙记录”中的“刷新日志”或打开窗口时，程序崩溃并报错：
`NameError: name 'QTableWidgetItem' is not defined`。

## 🔍 原因分析 (Analysis)
在 `src/ui/stats_window.py` 中，`QTableWidgetItem` 和 `QTableWidget` 目前是在 `init_tab_logs` 方法内部局部导入的。
然而，`refresh_logs` 方法也使用了 `QTableWidgetItem`，但在该方法的作用域内并没有导入这个类，导致 `NameError`。

虽然 Python 允许局部导入，但如果多个方法需要使用同一个类，最佳实践是将其放在文件顶部的导入区域。

## 🛠️ 修复方案 (Solution)
将 `QTableWidget`, `QTableWidgetItem`, `QHeaderView` 的导入从 `init_tab_logs` 方法内部移动到文件顶部的 `PyQt6.QtWidgets` 导入语句中。

## 📋 执行步骤 (Execution Steps)
- [x] **修改 `src/ui/stats_window.py`**:
    - 在顶部的 `from PyQt6.QtWidgets import ...` 中添加 `QTableWidget`, `QTableWidgetItem`, `QHeaderView`。
    - 删除 `init_tab_logs` 方法内部的局部导入语句。
- [x] **验证**:
    - 运行程序，打开“修仙记录”窗口。
    - 切换到“修仙日志”标签页。
    - 点击“刷新日志”按钮，确认不再报错且日志正常显示。

## 📝 验收标准 (Acceptance Criteria)
1. 打开 `StatsWindow` 不会立刻崩溃（因为 showEvent 会调用 refresh_logs）。
2. 点击刷新按钮能正常更新列表。

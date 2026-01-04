---
description: Implement UI fixes for Windows/Multi-screen, add Tray features, and add Event Logs.
---

# Plan 35: UI & UX Enhancements (界面与体验优化)

## 1. 目标 (Objectives)
根据用户反馈，本计划旨在修复 Windows 平台下的 UI 显示问题，优化多显示器支持，增强托盘功能，并新增持久化的历史事件日志。

## 2. 详细变更 (Changes)

### 2.1 修复秘籍输入 (Fix Secret Input)
**问题**: Windows 平台上 `QInputDialog` 的按钮文字可能不显示（白字白底或样式冲突）。
**方案**: 创建自定义的 `DarkInputDialog` 替代原生对话框，确保样式统一且在暗色主题下可读。
*   **新文件**: `src/ui/custom_input.py`
*   **修改**: `src/pet_window.py` 的 `input_secret` 方法。

### 2.2 多显示器支持 (Multi-monitor Support)
**问题**: 在多屏环境下，如果角色在副屏，打开的功能窗口（背包、坊市等）仍会出现在主屏。
**方案**: 修改窗口位置计算逻辑，基于当前 `PetWindow` 所在的屏幕来进行定位。
*   **修改**: `src/pet_window.py` -> `_calculate_safe_pos`。
    使用 `self.screen().geometry()` (PyQt6 推荐) 或 `QGuideApplication.screenAt(...)` 替代 `QApplication.primaryScreen()`。

### 2.3 托盘菜单增强 (Tray Menu)
**需求**: 增加“显示对话/事件”开关和“始终置顶”开关。
**方案**:
*   在 `PetWindow` 中添加对应的 Slot 方法：`set_always_on_top(bool)` 和 `toggle_notifications(bool)`。
*   在 `src/tray_icon.py` 中添加 Checkable Actions (可选菜单项)。
    *   [x] 始终置顶 (默认开启)
    *   [x] 显示气泡 (默认开启)

### 2.4 事件日志 (Event Logs)
**需求**: 在修炼记录中查看重要的历史事件。
**方案**:
*   **后端**: 确保关键事件（突破、获得稀有物品、特殊奇遇）被写入 `player_events` 表。
    *   检查并更新 `Cultivator` 或 `EventEngine` 的事件触发逻辑，调用 `db_manager.log_event(...)`。
*   **前端**: 在 `StatsWindow` (修炼记录) 中新增 "日志 (Logs)" 页签。
    *   显示最近的 50-100 条记录 (时间 | 类型 | 内容)。

## 3. 执行步骤 (Execution Steps)

1.  **UI 组件开发**: 创建 `src/ui/custom_input.py`。
2.  **核心逻辑修复**: 更新 `src/pet_window.py` 的输入框调用和多屏坐标计算。
3.  **托盘功能开发**: 更新 `src/tray_icon.py` 和 `src/pet_window.py` 的交互逻辑。
4.  **日志系统**:
    *   确认 `player_events` 表结构 (已存在)。
    *   在 `src/database.py` 中添加 `log_event` 和 `get_recent_events` 方法。
    *   在 `src/services/event_engine.py` 或 `cultivator.py` 中埋点记录日志。
    *   更新 `src/ui/stats_window.py` 添加日志页签。

## 4. 验证 (Verification)
*   **Windows**: 验证输入框文字是否清晰可见。
*   **多屏**: 将角色拖到副屏，打开背包，确认背包也在副屏显示且未超出边界。
*   **托盘**: 验证取消“始终置顶”后窗口是否可被遮挡；验证关闭气泡后是否不再弹窗。
*   **日志**: 触发几个事件后，在修炼记录中查看是否生效。

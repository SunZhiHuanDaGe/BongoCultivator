# Plan 5: 秘籍系统 (Cheat Codes)

## 目标
添加隐藏的作弊指令系统，允许玩家通过输入特定代码快速突破境界。

## 秘籍列表
1.  **代码**: `whosyourdaddy`
    *   **效果**: 立即突破至 **筑基期** (如果当前低于筑基)。
    *   **备注**: 经典魔兽争霸秘籍。
2.  **代码**: `上上下下左左右右baba`
    *   **效果**: 立即突破至 **金丹期** (如果当前低于金丹)。
    *   **备注**: 经典魂斗罗 Konami Code。

## 实现方案

由于全局监听键盘输入序列存在隐私风险且实现复杂，我们将采用 **右键菜单 -> 输入密令** 的方式，或者在特定窗口聚焦时监听。

**推荐方案**: 在右键菜单中增加一个隐藏或显式的入口。

### 步骤 1: UI 入口
在 `PetWindow` 的 context menu 中添加一个 "天机 (Secret)" 选项，或者在“关于”界面添加输入框。
或者，更隐蔽的方式：
- 在右键菜单底部添加一个 `Action("...", self)`。
- 点击后弹出一个 `QInputDialog`。

### 步骤 2: 逻辑处理
在 `src/cultivator.py` 或 `src/pet_window.py` 中处理输入字符串。

```python
def process_cheat_code(self, code):
    code = code.lower().strip()
    
    if code == "whosyourdaddy":
        # 目标: 筑基 (Layer 1)
        if self.cultivator.layer_index < 1:
            self.cultivator.layer_index = 1
            self.cultivator.exp = 0
            return "神力加持！你已直接晋升筑基期！"
            
    elif code == "上上下下左左右右baba":
        # 目标: 金丹 (Layer 2)
        if self.cultivator.layer_index < 2:
            self.cultivator.layer_index = 2
            self.cultivator.exp = 0
            return "魂斗罗附体！你已直接晋升金丹大道！"
            
    return "何方小辈竟敢窥视天道！速速退去！ (无效密令)"
```

### 步骤 3: 触发反馈
- 成功输入后，播放 `Tribulation` (渡劫) 特效或 `Success` 音效。
- 显示通知消息。

---
**Status**: Completed

## 完成情况 (Completion Log)
*Date: 2025-12-24*

### 1. 秘籍逻辑实现
- 在 `Cultivator` 中实现了 `process_secret_command`。
- 支持以下指令 (严格校验当前境界)：
    - `whosyourdaddy`: 炼气(0) -> 筑基(1)。
    - `上上下下左左右右baba`: 筑基(1) -> 金丹(2)。
    - `haiwangshabi`: 金丹(2) -> 元婴(3)。
    - `reborn`: 重置为初始状态。

### 2. UI 入口
- 在右键菜单底部添加了隐藏选项 "天机"。
- 点击弹出 `QInputDialog` 输入密令。
- 成功后触发突破音效/特效。

### 3. 验证
- 通过 `tools_verify_cheats.py` 验证了所有代码的生效条件和晋升逻辑。


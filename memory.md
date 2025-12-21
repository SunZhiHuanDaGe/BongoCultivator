# 项目记忆 (Project Memory)

## 核心架构 (Core Architecture)
- **GUI Framework**: PyQt6
- **架构模式**: 
    - `PetWindow` (View/Controller): 处理 UI、输入、动画渲染。
    - `Cultivator` (Model): 处理数据逻辑、属性计算、存档管理。
    - `InputMonitor`: 独立线程监控 APM。
    - `ItemManager` & `EventManager`: 单例管理数据配置。

## 已完成功能 (Completed Features)
1. **基础互动**: 
    - 鼠标拖拽移动
    - 鼠标点击播放随机对话
    - 右键菜单 (Context Menu)
    - 托盘图标控制 (System Tray) 与 "Ghost Mode" (鼠标穿透)
    - 窗口置顶且不抢占焦点

2. **修仙核心 (Cultivation Core)**:
    - **状态机**: IDLE (闭关), COMBAT (斗法), WORK (历练), READ (悟道) 基于 APM 自动切换。
    - **三维属性**: 
        - `Mind` (心魔): 影响修炼效率与渡劫成功率。
        - `Body` (体魄): 影响渡劫成功率。
        - `Affection` (好感): 影响掉落率。
    - **物品系统**: 
        - 物品分级 (Tier 1-2), 包含材料、消耗品、丹药。
        - 存/取/使用逻辑 (`InventoryWindow`)。
    - **炼丹系统**: 
        - 基于配方的炼丹界面 (`AlchemyWindow`)。
    - **随机事件**:
        - 定时触发 (默认 5分钟)，包含资源获取、状态变更。
    - **渡劫与天赋**:
        - 经验满后需手动渡劫 (成功率受属性影响)。
        - 渡劫成功获得天赋点，可升级 `Exp` (悟性) 或 `Drop` (机缘)。
        - `TalentWindow` 展示属性与加点。
    - **坊市系统**: 
        - 每日或手动刷新的随机商店。

## 数据存储 (Data Persistence)
- **文件**: `save_data.json`
- **内容**: 经验、境界、灵石、背包、市场数据、三维属性、天赋数据。
- **机制**: 程序关闭时自动保存，启动时读取；支持离线收益结算。

## 关键修复 (Critical Fixes)
- 修复了 `PetWindow` 初始化顺序导致的 `image_label` 属性丢失崩溃问题。
- 修复了 macOS 下窗口置顶与焦点抢占的冲突 (使用 `WindowDoesNotAcceptFocus`)。

## 下一步计划 (Next Steps)
- 详见 `plan2.md`

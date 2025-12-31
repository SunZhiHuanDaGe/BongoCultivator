# 🏗️ Project Structure & Architecture (项目结构与架构)

这份文档旨在为开发者提供项目的全景视图，帮助快速定位代码位置，理解模块间的交互关系，从而减少开发错误并对齐设计意图。

---

## 📂 目录结构 (Directory Layout)

```
BongoCultivator/
├── main.py                     # 🚀 程序入口 (Entry Point)
├── BongoCultivation-*.spec     # 📦 PyInstaller 打包配置文件 (Mac/Win)
├── assets/                     # 🎨 资源文件 (Images, Sounds)
├── user_data.db                # 💾 SQLite 数据库 (用户存档 + 静态数据)
├── docs/                       # 📚 文档中心
│   ├── plans/                  # 📅 开发计划 (Active/Archive)
│   ├── memory.md               # 🧠 项目核心记忆 (Architecture Notes)
│   └── STRUCTURE.md            # 📍 本文件 (You are here)
└── src/                        # 💻 源代码目录
    ├── cultivator.py           # [Core] 核心逻辑模型 (State, Exp, Attributes)
    ├── pet_window.py           # [Core] 主窗口控制 (Animation, Main Loop)
    ├── database.py             # [Data] 数据库管理 (Init, Migration)
    ├── input_monitor.py        # [System] 键鼠监听 (User Activity)
    ├── effect_widget.py        # [Visual] 粒子特效渲染组件
    │
    ├── services/               # 🛠 业务服务层 (Logic Services)
    │   ├── event_engine.py     # 事件引擎 (Trigger checks, Effect application)
    │   ├── achievement_manager.py # 成就管理
    │   └── ...
    │
    ├── ui/                     # 🖼 通用 UI 组件与统计窗口
    │   ├── base_window.py      # 窗口基类
    │   ├── stats_window.py     # 统计面板 (Matplotlib charts)
    │   └── merit_tab.py        # 功德/成就页签
    │
    └── [Feature Windows]       # 功能窗口 (直接位于 src 根目录下)
        ├── inventory_window.py # 储物袋 (Inventory)
        ├── alchemy_window.py   # 炼丹房 (Alchemy)
        ├── market_window.py    # 坊市 (Market)
        └── talent_window.py    # 天赋树 (Talents)
```

---

## 🧩 核心模块职责 (Module Responsibilities)

### 1. 核心循环 (Core Loop)
*   **`main.py`**: 初始化 `QApplication`，启动 `InputMonitor` 线程，加载数据库，并在 System Tray 创建图标。最后启动 `PetWindow`。
*   **`pet_window.py (PetWindow)`**:
    *   **角色**: 整个应用的 "Controller" 和 "View"。
    *   **职责**:
        *   维护一个 `QTimer` (通常 1秒/次) update 循环。
        *   处理鼠标点击、拖拽交互。
        *   管理动画状态 (`idle`, `walk`, `work` 等) 的切换。
        *   持有 `Cultivator` 实例，并调用其 `update()` 方法。
*   **`cultivator.py (Cultivator)`**:
    *   **角色**: 纯逻辑 "Model"。
    *   **职责**:
        *   计算 APM 并决定当前状态 (IDLE/WORK/READ/COMBAT)。
        *   计算 EXP 收益、属性变化 (Mind, Body)。
        *   调用 `EventEngine` 检查随机事件。
        *   管理背包数据 (调用 Database)。

### 2. 数据流 (Data Flow)
*   **SQLite (`user_data.db`)** 是唯一的事实来源。
*   **读取**: 启动时 `Cultivator` 从 DB `player_status`, `player_inventory` 加载数据到内存。
*   **写入**:
    *   关键事件 (如获得物品、突破) 立即写入。
    *   周期性数据 (如每分钟的 APM 统计) 由 `ActivityRecorder` 写入。
*   **静态数据**: 物品定义 (`items`) 和 事件定义 (`events`) 也存储在 DB 中，由 `tools/generate_json_assets.py` 或启动检查逻辑维护更新。

### 3. 事件系统 (Event System)
*   **`services/event_engine.py`**:
    *   根据 `Cultivator` 的上下文 (Layer, State, Attributes) 匹配数据库中的事件条件。
    *   执行事件结果 (Grant Item, Modify Stat)。
*   **流程**: `PetWindow` -> `Cultivator.update()` -> `EventEngine.check_trigger()` -> 返回 Event 对象 -> `PetWindow` 显示气泡通知。

---

## 📏 开发规范 (Development Guidelines)

1.  **路径引用**: 始终使用 **绝对路径** 或基于 `utils.get_resource_path` 的相对路径，确保打包后资源加载正常。
2.  **UI 开发**:
    *   新窗口尽量继承自 `src.ui.base_window.DraggableWindow` (如果存在) 或实现统一的拖拽逻辑。
    *   保持风格统一 (无边框, 透明背景, 右键菜单)。
3.  **数据变更**:
    *   增加新物品/事件：优先修改 `src/data/` 下的 JSON 定义或相关 Init 脚本，然后运行 Database Init 逻辑。
    *   修改数据库结构：务必在 `database.py` 中处理 Migration 逻辑。

---

## 🗺️ 如何按图索骥 (Navigation Guide)

*   **想修改数值/平衡性?** -> `src/cultivator.py` (EXP公式) 或 `src/data/items.json` (物品属性)。
*   **想加新功能窗口?** -> 参考 `src/inventory_window.py` 的实现，并在 `pet_window.py` 中绑定打开逻辑。
*   **想修动画/视觉?** -> `src/pet_window.py` (Sprite切换) 或 `src/effect_widget.py` (粒子特效)。
*   **想看以前的计划?** -> `docs/plans/archive/`。
*   **想看最新的任务?** -> `docs/plans/active/`。

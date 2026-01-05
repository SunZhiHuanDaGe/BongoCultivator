# Plan 46: 进度迁移系统 - "轮回转世"功能

## 问题背景 (Problem Context)

当前游戏存档使用 SQLite 数据库 (`user_data.db`)，存储在系统特定的用户数据目录下。虽然 Plan 22 实现了基础的文件迁移功能，但存在以下问题：

1. **表结构变化无法兼容**：当游戏版本更新导致数据库表结构变化（新增/删除/重命名字段）时，旧版 `.db` 文件无法被新版 SQLModel ORM 正确读取。
2. **跨平台迁移困难**：用户无法在不同设备（如从旧电脑换到新电脑）之间方便地迁移进度。
3. **Windows 用户高风险**：Windows 用户在更新游戏时更容易因覆盖安装或路径问题丢失进度。
4. **紧急备份需求**：用户需要一种"保险"方式来备份自己的进度，不依赖于数据库文件的完整性。

## 目标 (Goals)

实现一个**版本无关的进度导出/导入系统**，称为"**轮回转世**"功能：

1. **导出功能（"轮回留痕"）**：将当前完整进度导出为一个 `.json` 文件。
2. **导入功能（"转世归来"）**：从 `.json` 文件导入进度，覆盖当前存档。
3. **版本兼容**：导出格式为纯 JSON，不依赖特定数据库结构，可在任意未来版本中解析。
4. **UI 集成**：在托盘菜单中添加便捷入口。

## 技术设计 (Technical Design)

### 1. 导出文件格式定义

文件名：`BongoCultivator_Save_{timestamp}.json` 或用户自定义名称
扩展名：`.json`

**数据结构**：
```json
{
  "meta": {
    "version": "1.0",
    "game_version": "0.x.x",
    "export_time": 1704412800,
    "export_time_readable": "2026-01-05 11:30:00"
  },
  "player": {
    "layer_index": 3,
    "exp": 5000,
    "money": 12345,
    "body": 25,
    "mind": 10,
    "luck": 50,
    "talent_points": 5,
    "talents": {"exp": 2, "drop": 3},
    "death_count": 2,
    "legacy_points": 150,
    "equipped_title": "ach_keyboard_1",
    "daily_reward_claimed": "2026-01-05"
  },
  "inventory": {
    "t0_herb_001": 10,
    "t2_pill_003": 5
  },
  "used_once_items": ["t1_pill_special"],
  "achievements": [
    {"id": "ach_keyboard_1", "status": 2, "unlocked_at": 1704000000},
    {"id": "ach_clicks_1", "status": 2, "unlocked_at": 1704100000}
  ],
  "market": [
    {"id": "t1_herb_001", "price": 80, "discount": 0.8},
    {"id": "t2_pill_001", "price": 250, "discount": 1.0}
  ]
}
```

### 2. 核心模块设计

#### 2.1 新增文件：`src/services/progress_exporter.py`

```python
class ProgressExporter:
    """进度导出/导入管理器"""
    
    EXPORT_VERSION = "1.0"
    
    @staticmethod
    def export_progress(cultivator, filepath: str) -> tuple[bool, str]:
        """
        导出进度到 JSON 文件
        :return: (success, message)
        """
        pass

    @staticmethod
    def import_progress(cultivator, filepath: str) -> tuple[bool, str]:
        """
        从 JSON 文件导入进度
        :return: (success, message)
        """
        pass
    
    @staticmethod
    def validate_import_data(data: dict) -> tuple[bool, str]:
        """
        验证导入数据的基本结构
        """
        pass
```

#### 2.2 修改文件：`src/tray_icon.py`

在托盘菜单中添加新的子菜单 "轮回转世"，包含：
- "轮回留痕 (导出进度)" - 触发文件保存对话框
- "转世归来 (导入进度)" - 触发文件选择对话框

#### 2.3 UI 交互流程

**导出流程**：
1. 用户点击 "轮回留痕"
2. 弹出文件保存对话框，默认文件名 `BongoCultivator_Save_YYYYMMDD_HHMMSS.json`
3. 保存成功后弹出提示 "轮回之力已封印！进度已保存至：{filepath}"

**导入流程**：
1. 用户点击 "转世归来"
2. 弹出确认对话框 "此操作将覆盖当前所有进度！是否继续？"
3. 用户确认后，弹出文件选择对话框（过滤 `.json` 文件）
4. 验证文件格式，导入成功后重新加载数据并刷新 UI
5. 弹出提示 "轮回成功！道友已返归本源。"

## 实施步骤 (Implementation Steps)

### ✅ 步骤 1：创建 ProgressExporter 服务

文件：`src/services/progress_exporter.py`

实现 `export_progress()` 方法：
- 从 Cultivator 实例读取所有核心属性
- 从数据库读取成就列表
- 构建标准化 JSON 结构
- 写入文件

实现 `import_progress()` 方法：
- 读取 JSON 文件
- 验证必需字段存在
- 更新 Cultivator 实例属性
- 更新数据库（PlayerStatus, PlayerInventory, Achievements 等）
- 触发 `save_data()` 确保持久化

### ✅ 步骤 2：修改托盘菜单

文件：`src/tray_icon.py`

- 添加子菜单 "轮回转世"
- 添加两个 Action：导出/导入
- 连接到 PetWindow 的新方法（因为需要访问 Cultivator）

### ✅ 步骤 3：在 PetWindow 中添加导出/导入触发方法

文件：`src/pet_window.py`

- 添加 `trigger_export_progress()` 方法：弹出保存对话框，调用 ProgressExporter
- 添加 `trigger_import_progress()` 方法：弹出确认和选择对话框，调用 ProgressExporter，重新加载并刷新 UI

### 步骤 4：测试验证

1. **导出测试**：正常游玩后导出，检查 JSON 文件内容完整性
2. **导入测试**：
   - 新建空档后导入，验证进度恢复
   - 在有进度的存档上导入，验证覆盖成功
3. **版本兼容测试**：模拟未来版本增加新字段，确保旧导出文件仍可导入（新字段取默认值）
4. **跨平台测试**：macOS 导出的文件在 Windows 上导入（需人工验证）

## 边界情况处理 (Edge Cases)

1. **导出时游戏数据未加载**：返回错误提示
2. **导入的 JSON 格式错误**：验证失败，提示用户
3. **导入的 JSON 缺少必需字段**：使用默认值补全，记录警告日志
4. **物品 ID 在新版本中不存在**：保留原 ID，日志警告（不删除物品数据）
5. **成就 ID 在新版本中不存在**：跳过该成就，日志警告

## 名词定义 (Terminology)

| 游戏内名称 | 功能 |
|----------|------|
| 轮回转世 | 菜单名称 (子菜单) |
| 轮回留痕 | 导出进度 |
| 转世归来 | 导入进度 |

## 文件变更清单 (Files to Modify)

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `src/services/progress_exporter.py` | **新增** | 导出/导入核心逻辑 |
| `src/tray_icon.py` | 修改 | 添加托盘菜单入口 |
| `src/pet_window.py` | 修改 | 添加导出/导入触发方法 |
| `docs/memory.md` | 修改 | 记录新功能 |

---
**预计工作量**: 1-2 小时
**优先级**: 高 (用户需求驱动)

---

## ✅ 完成状态

- **完成时间**: 2026-01-05 11:45
- **实现内容**:
  - ✅ 创建 `ProgressExporter` 服务类，实现 JSON 格式的进度导出/导入
  - ✅ 托盘菜单添加"轮回转世"子菜单（轮回留痕/转世归来）
  - ✅ PetWindow 添加触发方法，支持文件对话框和确认对话框
  - ✅ 更新 memory.md 和 PLANS_README.md 文档
- **测试验证**: 代码加载验证通过，需用户手动测试功能

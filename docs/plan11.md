# Plan 11: 成就系统 (Achievements)

## 目标
利用已有的生产力统计数据 (`ActivityRecorder`)，为用户的现实行为（工作/摸鱼）提供游戏内的正向反馈。

## 1. 数据库设计 (`achievements`)

```sql
CREATE TABLE achievements (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    condition_type TEXT,    -- total_keys, total_clicks, total_hours, max_apm
    threshold INTEGER,      -- 达成数值
    reward_json TEXT,       -- {"type": "title", "value": "键道宗师"}
    is_unlocked INTEGER DEFAULT 0,
    unlocked_at INTEGER
);
```

## 2. 成就设计
- **键道系列 (Keystrokes)**:
    - **初窥门径**: 累计敲击 10,000 次。
    - **键气纵横**: 累计敲击 100,000 次。
    - **人键合一**: 累计敲击 1,000,000 次 -> 奖励称号 "键仙"。
- **修仙时长 (Idle Time)**:
    - **闭关锁国**: 累计运行 24 小时。
    - **沧海桑田**: 累计运行 100 小时 -> 奖励永久属性 "定力" (心魔增长减慢)。
- **爆发力 (Max APM)**:
    - **触手怪**: 单分钟 APM 超过 500。

## 3. 系统实现 (`src/services/achievement_manager.py`)
- **监听**: 每次 `ActivityRecorder` 写入数据后，触发在此 Check。
- **状态维护**: 内存中缓存已解锁列表，避免重复弹窗。
- **UI 展示**:
    - **通知**: 达成时弹出金色通知 "解锁成就：[键道宗师]！"。
    - **面板**: 在 `StatsWindow` 或 `TalentWindow` 中增加 "成就" Tab，展示徽章列表。

## 4. 执行步骤
1.  **Schema**: 创建表。
2.  **Logic**: 编写检测逻辑。
3.  **UI**: 制作成就图标 (可复用现有资源或文字徽章)，集成到界面。

---
**Status**: Pending

# Plan 11: 天道功德榜 (Heavenly Merit System)

## 1. 核心理念 (Core Concept)

> **"凡有所相，皆是虚妄；唯有因果，真实不虚。"**

将传统的 "Achievements" 包装为 **"天道功德 (Heavenly Merit)"** 系统。
用户的每一次敲击、每一分钟挂机、每一个触发的奇遇，都会在冥冥之中积累"因果"。
当因果达到临界点，天道会降下**"功德碑" (Merit Stele)** 赐予封号与宝物。

**设计原则**:
1.  **沉浸感**: 不弹 "Achievement Unlocked"，而是弹 "天道感应 (Heavenly Resonance)"。
2.  **物质奖励**: 强关联 `docs/plan9.md` 的物品系统，成就即是获取稀有资源的途径。
3.  **称号系统**: 获得的封号不仅仅是文字，更可佩戴并提供微量属性加成（如：修炼速度、掉率）。
4.  **高性能**: 拒绝每帧检查。基于 `ActivityRecorder` 的聚合数据 + 事件驱动触发。

---

## 2. 数据库设计 (`achievements`)

在 `user_data.db` 中新建表。

```sql
CREATE TABLE achievements (
    id TEXT PRIMARY KEY,        -- e.g., 'ach_kb_10k'
    category TEXT,              -- 'action'(行道), 'time'(岁月), 'chance'(机缘), 'fortune'(财阀)
    name TEXT,                  -- 显示名称, e.g. "剑意初成"
    desc TEXT,                  -- 描述
    condition_type TEXT,        -- 'stat_total', 'action_count', 'item_count', 'event_trigger'
    condition_target TEXT,      -- 目标键值
    threshold INTEGER,          -- 目标数值
    reward_type TEXT,           -- 'title', 'item', 'buff'
    reward_value TEXT,          -- 物品ID 或 称号定义 JSON
    is_hidden INTEGER DEFAULT 0,-- 是否为隐藏成就
    status INTEGER DEFAULT 0,   -- 0: Locked, 1: Completed, 2: Claimed
    unlocked_at INTEGER
);

-- 新增：用户佩戴称号字段需在 user_state 表中添加 'equipped_title'
```

---

## 3. 成就图谱 (The Merit Roll)

### 3.1 行道 (Dao of Action) - 键鼠操作
*以力证道，不仅看数量，更看操作习惯。*

| ID | 名称 | 类型 | 条件 | 奖励 (Resonance) | 备注 |
|:---|:---|:---|:---|:---|:---|
| `ach_kb_1w` | **剑意初成** | Grind | Keyboard > 10,000 | Item: `ore_iron_essence` x1 | 基础 |
| `ach_kb_100w`| **一剑开天门**| Grind | Keyboard > 1,000,000| Title: **[剑仙]** (攻击+5%) | 长期目标 |
| `ach_mouse_5w`| **指点江山** | Grind | Mouse > 50,000 | Item: `part_wolf_tooth` x10 | - |
| `ach_apm_400` | **唯快不破** | Skill | Max APM > 400 | Item: `part_spider_silk` x10 | 爆发力 |
| `ach_back_1k` | **悔棋者** | Meta | Backspace Key > 1,000 | Title: **[时光回溯]** (闪避+1%) | 撤销即后悔 |
| `ach_enter_5k`| **一锤定音** | Meta | Enter Key > 5,000 | Item: `ore_copper_red` x5 | 确认即决心 |
| `ach_combo_1h`| **人键合一** | Flow | 持续操作1小时(无>1m中断)| Title: **[入定]** (修炼效率+2%)| 专注工作 |

### 3.2 岁月 (Dao of Time) - 挂机与作息
*感悟光阴流逝，奖励规律生活或极致修仙。*

| ID | 名称 | 类型 | 条件 | 奖励 (Resonance) | 备注 |
|:---|:---|:---|:---|:---|:---|
| `ach_time_24h`| **初窥门径** | Idle | Uptime > 24 Hours | Item: `pill_detox_0` x1 | - |
| `ach_time_100h`| **沧海桑田** | Idle | Uptime > 100 Hours | Item: `stone_three_life` x1 | - |
| `ach_work_late`| **守夜人** | Hidden | 凌晨 3:00-4:00 有操作 | Title: **[夜游神]** (暗夜掉率up) | 熬夜修仙 |
| `ach_early_bird`| **闻鸡起舞** | Habit | 早晨 5:00-7:00 有操作 | Item: `water_dew_morning` x5 | 晨露好收集 |
| `ach_weekend` | **无休居士** | Habit | 周六/日 累计操作>4小时 | Item: `pill_strength_bary` x2 | 加班狂魔 |
| `ach_afk_long`| **神游太虚** | Idle | 挂机 > 2小时 无操作 | Title: **[顽石]** (防御+2%) | 真正的摸鱼 |

### 3.3 机缘 (Dao of Chance) - 事件与运气
*天道无常，祸福相依。*

| ID | 名称 | 类型 | 条件 | 奖励 (Resonance) | 备注 |
|:---|:---|:---|:---|:---|:---|
| `ach_evt_100` | **红尘炼心** | Count | Trigger Events > 100 | Item: `pill_luck_minor` x2 | 见多识广 |
| `ach_fail_5` | **道心弥坚** | Fail | 突破/渡劫失败 > 5次 | Title: **[百折不挠]** (抗心魔) | 失败是成功之母 |
| `ach_die_1` | **兵解重修** | Fail | 心魔爆炸/死亡 x1 | Item: `pill_reborn_heaven` x1 | - |
| `ach_rare_drop`| **天命所归** | Luck | 获得 Tier 7+ 物品 x1 | Title: **[气运之子]** (掉率+5%) | 欧皇认证 |
| `ach_trash_king`| **垃圾佬** | Collection| 收集 Junk 类物品 > 50 | Item: `bag_storage_runes` (扩容)| 变废为宝 |
| `ach_monster_sl`| **除魔卫道** | Combat | 处于 Combat 状态 > 10h | Item: `beast_core_gold` x1 | 战斗狂人 |

### 3.4 财阀 (Dao of Wealth) - 灵石与其消耗
*财侣法地，财字当头。*

| ID | 名称 | 类型 | 条件 | 奖励 (Resonance) | 备注 |
|:---|:---|:---|:---|:---|:---|
| `ach_rich_1w` | **腰缠万贯** | Saving | Spirit Stones > 10,000 | Title: **[多宝道人]** (灵石获取+5%)| - |
| `ach_rich_100w`| **富可敌国**| Saving | Spirit Stones > 1,000,000| Item: `metal_taiyi` x1 | 顶级富豪 |
| `ach_poor_0` | **身无分文** | Hidden | Stone < 10 (Total>1k) | Item: `misc_broken_sword` x1 | 乞丐体验 |
| `ach_spend_5k`| **挥金如土** | Spending | Store Spend > 5,000 | Item: `pill_beauty_face` x1 | 消费回馈 |
| `ach_sell_100`| **陶朱公** | Trade | Sell Items > 100 | Title: **[精算师]** (售价+5%) | 商人本色 |
| `ach_hoard_90`| **仓鼠精** | Storage | 背包占用 > 90% | Item: `soil_chaos` (息壤) x1 | 空间不够自己造 |

---

## 4. 称号系统 (Title System)

称号不仅仅是 UI 上的展示，它被视为一种特殊的 **"法相" (Dharma Aspect)**。

### 4.1 核心逻辑
1.  **Unique**: 同一时间只能佩戴一个称号。
2.  **Display**: 佩戴后，在 Dashbaord 角色名旁显示 `[称号]`，并可能有特殊字体颜色/光效。
3.  **Effect**: 称号携带 `passive_buff`，在 `Cultivator` 的 `_apply_buffs` 环节生效。

### 4.2 UI 交互设计
*   在 `StatsWindow` (状态面板) 或 `TalentWindow` 中新增 **[功德簿] (Merit Book)** 标签页。
*   **左侧列表**: 分类显示成就 (行道/岁月/机缘/财阀)。
    *   *Locked*: 灰色，显示进度条 (e.g., "Keyboard: 5432/10000")。
    *   *Unlocked*: 金色高亮，点击可领取奖励。
    *   *Claimed*: 变暗，若奖励是称号，显示 "Equip/Unequip" 按钮。
*   **顶部展示**: 当前佩戴称号预览。

### 4.3 代码结构变化
*   **`Cultivator` Class**:
    *   新增属性 `self.equipped_title: str = None` (存储 Title ID)。
    *   新增方法 `equip_title(title_id)`, `unequip_title()`.
    *   修改 `get_stats()`: 动态计算属性时，需叠加 `TitleManager.get_buff(self.equipped_title)` 的效果。

---

## 5. 系统实现 (Architecture)
*(保持原有的 Check 时机与 AchievementManager 设计)*

### 5.1 数据流
1.  `ActivityRecorder` 更新数据 -> `AchievementManager.check_periodic()` (Cron).
2.  用户操作 (Sell/Events) -> `AchievementManager.check_trigger(type, val)`.
3.  `check` 发现新完成 -> Update DB -> `NotificationSystem.show("天道感应")`.
4.  用户打开 UI -> `AchievementManager.get_all()` -> 前端渲染列表.
5.  用户点击 Equip -> API `/api/cultivator/equip_title` -> Update User State -> Refresh Stats.

---
**Status**: Completed

## 完成情况 (Completion Log)
*Date: 2025-12-25*

### 1. 数据库与数据注入
- 创建了 `achievements` 表，包含 id, category, name, desc, condition, threshold, reward 等字段。
- 为 `player_status` 表增加了 `equipped_title` 字段用于存储当前佩戴的称号。
- 编写并执行了 `tools/init_achievements.py`，预置了 25 个成就，涵盖 **行道(Action)**, **岁月(Time)**, **机缘(Chance)**, **财阀(Fortune)** 四大类。

### 2. 后端逻辑
- 实现了 `AchievementManager` (`src/services/achievement_manager.py`)：
    - **Check Logic**: 支持基于 `ActivityLogs` 聚合数据的定期检查 (check_periodic) 和基于特定触发器的即时检查 (check_trigger)。
    - **Title Buffs**: 定义了 9 种称号及其 Buff 效果 (e.g. `[剑仙]` 增加修为获取, `[夜游神]` 增加夜间掉率)。
    - **Unlock & Claim**: 实现了成就解锁、奖励领取 (物品自动入包、称号解锁状态更新) 的完整流程。
- 更新了 `Cultivator` (`src/cultivator.py`)：
    - 集成了 `equipped_title` 的佩戴与卸下逻辑。
    - 在 `update()` 循环中应用了称号带来的 `exp_mult` 和 `drop_mult` 加成。
    - 在每次获得经验后自动检查成就进度，并触发 "天道感应" 通知。

### 3. 前端 UI
- 创建了 `MeritTab` (`src/ui/merit_tab.py`)：
    - 展示当前佩戴的法相 (Title)。
    - 提供分类筛选 (All/Action/Time/Chance/Fortune)。
    - 列表展示成就卡片，支持查看进度、领取奖励、佩戴称号。
- 更新了 `StatsWindow` (`src/ui/stats_window.py`)，新增了 "功德簿" 标签页。

### 4. 验证
- 数据库 schema 更新成功。
- 数据注入脚本执行成功 (25 added)。
- 代码整合无误。

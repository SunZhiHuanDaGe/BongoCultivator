# Plan 12: 视觉素材更新与全境界渡劫设计 (Visual Assets & Tribulations)

## 1. 目标 (Goal)
基于最新的 1024x1024 高清像素风格 (High-res Pixel Art)，更新现有美术素材，并特别为 **9个大境界的突破** 设计独有的渡劫/晋升画面，增强游戏的视觉反馈与成就感。

## 2. 基础素材清单 (Basic Assets)
*(沿用 Plan 11 内容，确保基础状态完整)*

*(沿用 Plan 11 修改后的完整 Prompt)*

| 状态/功能 | 文件名 (Asset Name) | 说明 |
| :--- | :--- | :--- |
| **待机** | `cultivator_idle.png` | 基础站立呼吸 |
| **行走** | `cultivator_walk.png` | 移动循环帧 |
| **阅读** | `cultivator_read.png` | 手持卷轴阅读 |
| **工作** | `cultivator_work.png` | 操控浮空键盘/飞剑 |
| **战斗** | `cultivator_combat.png` | 施法战斗姿态 |
| **炼丹** | `cultivator_alchemy.png` | 炼丹炉场景 |
| **拖拽** | `cultivator_drag.png` | 被拎起来 |
| **睡觉** | `cultivator_sleep.png` | 打坐/睡觉 |

### 📂 基础状态 (Basic States)

#### 1. 待机 (Idle)
*文件名: `cultivator_idle.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Standing in a relaxed idle pose, breathing calmly, hands resting naturally by sides, facing forward.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 2. 行走 (Walk)
*文件名: `cultivator_walk.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Walking forward cycle, dynamic confident stride, side view or 3/4 view.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 3. 悟道/阅读 (Read)
*文件名: `cultivator_read.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Floating or sitting, holding an ancient bamboo scroll or mystical book, reading intently with magical runes floating around.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 4. 历练/工作 (Work)
*文件名: `cultivator_work.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Focused expression, typing rapidly on a magical floating glowing keyboard made of spiritual energy, or controlling multiple flying paper talismans.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 5. 斗法/战斗 (Combat)
*文件名: `cultivator_combat.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Dynamic combat pose, casting a powerful spell, one hand pointing forward with sword fingers, glowing blue energy gathering, robes flowing wildly.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 6. 炼丹 (Alchemy)
*文件名: `cultivator_alchemy.png`*
**版本 A (基础)**:
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Sitting cross-legged, fanning a fire under a small simple copper pot, cooking medicinal herbs, light steam rising.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```
**版本 B (高阶)**:
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Casting magic spells in front of a massive, ornate golden furnace (Ding) with dragon carvings. The furnace is glowing with magical purple and blue aura.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 7. 被拖拽 (Drag)
*文件名: `cultivator_drag.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Being picked up by the back of the collar (dangling), limbs hanging down or struggling comically, surprised expression.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

#### 8. 睡觉 (Sleep)
*文件名: `cultivator_sleep.png`*
```text
(Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun.
ACTION: Sleeping peacefully on a cloud or a straw mat, snot bubble appearing, Zzz particles.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset.
(Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
```

---

## 3. 全境界渡劫特效设计 (Realm-Specific Tribulation Scenes)
**文件名格式**: `tribulation_lv{Level}_to_{NextLevel}.png`
**设计理念**: 随着境界提升，画面从平静的运气，逐渐演变为各种天地异象，最终飞升。

### 🎨 必选通用描述 (Consistency Block)
**请在每个 Prompt 中包含以下段落：**
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.

---

### Phase 1: 下境界 (Lower Realms)

#### Lv0 → Lv1: 筑基 (Foundation Establishment)
*文件名: `tribulation_0_foundation.png`*
**描述**: 气旋凝聚，尘土飞扬，初窥门径。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Sitting in lotus position, concentrating hard. Swirling white mist and gentle wind currents surround the character. Small blue spiritual sparks are gathering around the body. Ground has small dust clouds.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

## Execution Log

*   **2025-12-25**: Plan created. Phase 1 assets (Lv0-Lv2) generated and integrated.
*   **2025-12-25**: Processed transparency for Phase 1 assets.
*   **2025-12-25**: Generated Phase 2 & 3 assets (Lv3-Lv8).
*   **2025-12-25**: Fixed critical bug where tribulation animation was skipped due to duplicate function definitions and game loop race conditions. Implemented robust `is_ascending` lock and state priority.
*   **2025-12-25**: All assets verified and transparency processed. Tribulation system fully operational.

#### Lv1 → Lv2: 金丹 (Golden Core)
*文件名: `tribulation_1_goldcore.png`*
**描述**: 丹田结丹，金光外溢。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Floating slightly off the ground. A brilliant, glowing golden orb (Golden Core) is forming visible in the chest area/dantian. Golden rays of light burst outward from the center. Clothes flapping in energy.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

#### Lv2 → Lv3: 元婴 (Nascent Soul)
*文件名: `tribulation_2_nascentsoul.png`*
**描述**: 碎丹成婴，元神出窍。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Meditating with eyes closed. A tiny, translucent, glowing mini-version of the cultivator (Nascent Soul) is emerging/floating just above the character's head. Soft blue spiritual pressure waves ripple outward.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

---

### Phase 2: 中境界 (Middle Realms) - [Completed]

#### Lv3 → Lv4: 化神 (Divine Transformation)
*文件名: `tribulation_3_divine.png`*
**描述**: 神念通达，身化万千。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Character is glowing with an intense divine white aura. Two spectral blue afterimages or clones appear faintly behind the character (showing speed/omnipresence). Eyes glowing pure white without pupils.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

#### Lv4 → Lv5: 炼虚 (Void Refining)
*文件名: `tribulation_4_void.png`*
**描述**: 破碎虚空，空间扭曲。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Floating in a chaotic stance. Surrounding the character are dark purple void cracks and spatial distortions (glitches). Small rocks are floating upward against gravity. Mysterious starry void background patches.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

#### Lv5 → Lv6: 合体 (Integration)
*文件名: `tribulation_5_integration.png`*
**描述**: 法身合一，返璞归真。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: The character's body looks partially elemental or translucent, merging with nature. Surrounded by a mix of fire, water, and wind elements swirling in harmony. A rainbow-colored aura surrounds the body.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

---

### Phase 3: 上境界 (Upper Realms) - [Completed]

#### Lv6 → Lv7: 大乘 (Mahayana / Great Vehicle)
*文件名: `tribulation_6_mahayana.png`*
**描述**: 功德圆满，步步生莲。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Standing peacefully with a benevolent expression. Golden lotus flowers are blooming on the ground around the feet. Five-colored divine clouds (Xiangyun) are descending from above. Soft, holy radiant light.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

#### Lv7 → Lv8: 渡劫 (Tribulation / Calamity)
*文件名: `tribulation_7_calamity.png`*
**描述**: 九霄雷劫，生死一线。**最激烈的画面**。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Looking up in defiance at a terrifying dark thundercloud above. Striking thick red and purple lightning bolts are hitting a magical energy shield the character is holding up. Intense dramatic lighting, gritty expression.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```
**Status**: Completed
**Priority**: High
**Dependencies**: Plan 11 (Achievements) - Completed, Plan 13 (Tribulation Logic) - Completed

#### Lv8 → Lv9: 飞升 (Ascension)
*文件名: `tribulation_8_ascension.png`*
**描述**: 天门大开，羽化登仙。
```text
> (Character) A cute chibi cultivator character, wearing white traditional Hanfu robes with blue trim, black hair styled in a Daoist topknot bun. (Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline, 2D game sprite asset. (Technical) Solid white background, crisp pixels, no anti-aliasing, sharp edges, isolated subject.
(Character) [Insert Consistency Block Here]
ACTION: Flying upwards towards a massive opening golden Heavens Gate in the sky. A golden staircase appears. The character's lower body is dissolving into particles of light (ascending). Celestial cranes flying around.
(Style) High-res pixel art style, 1024x1024 resolution, thick black contour outline. Solid white background.
```

---

## 4. 补充说明
- **通用 Prompt**: 在生成时，请务必将 `[Insert Consistency Block Here]` 替换为你在 `plan11` 中确定的那段固定描述。
- **背景处理**: 所有图片必须是 `Solid white background`，方便游戏内透明化调用。
- **特效层级**: 低境界特效少，高境界特效多且华丽，色彩从单色（蓝/白）向金、紫、七彩过渡。

最后可以用tools/process_images.py 来完成图片空白部分的处理。
# 🧘 BongoCultivator (修仙桌宠)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-green.svg)]()

<p align="center">
  <img src="assets/cultivator_idle.png" alt="BongoCultivator" width="200">
</p>

<p align="center">
  <strong>在敲键盘中历练筋骨，在点鼠标中斩妖除魔，在摸鱼中打坐悟道。</strong><br>
  你的桌面，就是你的修仙洞府。
</p>

---

## ✨ 核心特色

### ⌨️ 赛博修炼
你的每一次键盘敲击、鼠标点击都会被系统捕获并转化为修为：
- **闭关 (Idle)**: 摸鱼时自动积累修为
- **历练 (Work)**: 敲键盘（写代码/文档）收益提升
- **悟道 (Read)**: 频繁鼠标操作时触发顿悟
- **斗法 (Combat)**: 极高 APM 进入战斗模式

### 🐱 桌面陪伴
一只可爱的修仙小人常驻桌面：
- 始终置顶但不抢占焦点
- 背景透明、可自由拖拽
- 多种状态动画（呼吸、施法、炼丹）
- 粒子特效（雷劫、火焰、金光）

### ⚗️ 炼丹系统
- **121 种物品** (Tier 0 - Tier 8)
- **42 种丹方** 可供炼制
- **坊市交易** 每 15 分钟刷新

### 🎲 随机奇遇
- **66+ 种事件** 随时触发
- 根据境界和状态解锁不同事件
- 完整的修仙日志记录

### 🏆 成就系统
- 20+ 成就解锁专属头衔
- 头衔提供永久属性加成

---

## 🎮 九重境界

```
炼气期 → 筑基期 → 金丹期 → 元婴期 → 化神期 → 炼虚期 → 合体期 → 大乘期 → 渡劫期 → ✨ 飞升仙界
```

---

## 🚀 快速开始

### 方式一：下载预编译版本（推荐）

前往 [Releases](https://github.com/robinshi2010/BongoCultivator/releases) 页面下载：
- **macOS**: `BongoCultivator.app`
- **Windows**: `BongoCultivator.exe`

### 方式二：源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/robinshi2010/BongoCultivator.git
cd BongoCultivator

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 运行
python3 main.py
```

### 依赖项
- Python 3.10+
- PyQt6
- pynput
- matplotlib
- pillow
- sqlmodel

---

## 🎮 操作指南

| 操作 | 说明 |
|------|------|
| **左键拖拽** | 移动小人位置 |
| **左键点击** | 播放修仙对话 |
| **右键点击** | 打开功能菜单 |

### 功能菜单
- 📊 **状态** - 查看详细属性
- 🎒 **储物袋** - 查看物品、使用丹药
- ⚗️ **炼丹房** - 合成丹药
- 🏪 **坊市** - 购买材料
- 📈 **统计** - 工作效率图表
- ⚙️ **设置** - 系统选项

---

## 🛠 技术栈

| 组件 | 技术 |
|------|------|
| **语言** | Python 3.10+ |
| **GUI** | PyQt6 |
| **数据库** | SQLite + SQLModel |
| **图表** | Matplotlib |
| **输入监听** | Pynput |
| **打包** | PyInstaller |

---

## 📂 项目结构

```
BongoCultivator/
├── main.py              # 程序入口
├── requirements.txt     # 依赖声明
├── LICENSE              # CC BY-NC-SA 4.0
├── assets/              # 资源文件
│   ├── cultivator_*.png # 角色状态图
│   └── tribulation_*.png# 渡劫特效图
└── src/                 # 源代码
    ├── cultivator.py    # 核心逻辑
    ├── data/            # 静态数据 (JSON)
    ├── models/          # 数据模型
    ├── services/        # 业务服务
    ├── ui/              # UI 组件
    └── utils/           # 工具函数
```

---

## 📜 许可证

本项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 协议。

✅ 免费使用和分享  
✅ 可以修改代码  
❌ **禁止商业使用**  
🔄 修改版须使用相同协议

---

## 🤝 贡献

欢迎提交 Issue 或 PR！

如果你有：
- 有趣的修仙事件文案
- 新的丹药点子
- Bug 反馈

请在 [Issues](https://github.com/robinshi2010/BongoCultivator/issues) 中留言。

---

## 📧 联系

- GitHub: [@robinshi2010](https://github.com/robinshi2010)

---

<p align="center">
  <strong>愿道友早日飞升 🌟</strong>
</p>

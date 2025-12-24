# Plan 8: 跨平台打包与发布 (Packaging & Distribution)

## 目标
将 Python 源代码打包为独立的可执行文件，方便没有 Python 环境的用户安装和使用。
- **macOS**: 生成 `.app` 应用包，可选制作 `.dmg` 镜像。
- **Windows**: 生成 `.exe` 可执行文件，可选制作安装向导。

## 1. 技术选型
使用 **PyInstaller** 作为核心打包工具。它支持 PyQt6 并且能很好地处理跨平台依赖。

## 2. 准备工作

### 2.1 依赖检查
确保 `requirements.txt` 完整 (已包含 PyQt6, pynput)。
安装打包工具:
```bash
pip install pyinstaller
```

### 2.2 资源路径处理 (重要)
在代码中 (`pet_window.py`, `item_manager.py` 等) 涉及读取 `assets/` 或 `data/` 的地方，必须适配 PyInstaller 的临时解压路径 (`sys._MEIPASS`)。

**通用路径辅助函数**:
```python
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
```
*需要在所有文件读取逻辑中替换此函数。*

---

## 3. macOS 打包流程

### 3.1 生成 Spec 文件
```bash
pyi-makespec --windowed --name "BongoCultivation" --icon="assets/icon.icns" --add-data="assets:assets" --add-data="src/data:src/data" main.py
```
*注: `--windowed` 避免出现终端窗口。*

### 3.2 权限配置 (macOS 特有)
由于使用了 `pynput` (输入监听)，打包后的应用需要申请 **辅助功能 (Accessibility)** 和 **输入监听 (Input Monitoring)** 权限。
- 可能需要修改 `Info.plist` (PyInstaller 可以在 spec 中注入)。
- 未签名的应用在其他人的 Mac 上运行可能会提示“已损坏”，需要执行 `xattr -cr /Applications/BongoCultivation.app` 或进行开发者签名。

### 3.3 执行打包
```bash
pyinstaller BongoCultivation.spec
```

### 3.4 制作 DMG (可选)
使用 `create-dmg` 工具:
```bash
create-dmg \
  --volname "Bongo Cultivation Installer" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "BongoCultivation.app" 200 190 \
  --hide-extension "BongoCultivation.app" \
  --app-drop-link 600 185 \
  "BongoCultivation-Installer.dmg" \
  "dist/BongoCultivation.app"
```

---

## 4. Windows 打包流程

### 4.1 生成 Spec 文件
与 Mac 类似，但图标格式为 `.ico`，路径分隔符自动处理。
```bash
pyi-makespec --windowed --name "BongoCultivation" --icon="assets/icon.ico" --add-data="assets;assets" --add-data="src/data;src/data" main.py
```
*注意: Windows 下 `--add-data` 分隔符为分号 `;`，而 Mac/Linux 为冒号 `:`。*

### 4.2 执行打包
```bash
pyinstaller BongoCultivation.spec
```

### 4.3 制作安装包 (可选)
为了显得更正式，使用 **Inno Setup** 制作 `setup.exe`。
- 编写 `.iss` 脚本，定义安装目录、桌面快捷方式等。
- 编译生成 `Bongo_Setup_v1.0.exe`。

---

## 5. 执行顺序

1.  **代码适配**: 修改所有涉及路径的代码，使用 `get_resource_path`。
2.  **图标制作**: 准备 `icon.icns` (Mac) 和 `icon.ico` (Win)。
3.  **本地测试**: 在当前开发机 (Mac) 先跑通 Mac 打包。
4.  **Windows 环境**: 若需要 Windows 包，需要在 Windows 机器 (或虚拟机) 上重复上述步骤 (Python 代码通用的，但 PyInstaller 必须在目标系统上运行)。

---
**Status**: Pending Implementation

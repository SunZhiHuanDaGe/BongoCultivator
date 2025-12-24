import sys
import os

def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径。
    支持 Dev 环境和 PyInstaller 打包环境 (_MEIPASS)。
    :param relative_path: 相对路径 (例如 'assets/icon.png' 或 'src/data/items.json')
    :return: 绝对路径
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        # 开发环境: 项目根目录
        # 假设此文件在 src/utils/path_helper.py -> ../.. 是根目录
        # 但这也取决于 relative_path 是相对于谁。
        # 通常我们约定 relative_path 是相对于项目根目录 (bongo/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(os.path.dirname(current_dir))
        
    return os.path.join(base_path, relative_path)

def get_user_data_dir():
    """
    获取用户数据存储目录 (用于存档数据库等)。
    在 Mac 上通常是 ~/Library/Application Support/BongoCultivation
    在 Win 上是 AppData/Local/...
    或者为了简单，如果是 Portable 模式，就放在可执行文件旁边。
    
    这里我们暂时使用简单的策略：
    1. 开发环境: 项目根目录
    2. 打包环境: 可执行文件所在目录 (sys.executable 的 dirname)
    """
    if hasattr(sys, '_MEIPASS'):
        # 打包环境，使用 exe 所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(os.path.dirname(current_dir))

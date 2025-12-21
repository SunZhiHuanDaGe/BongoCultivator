import sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal

class SystemTray(QObject):
    # 信号：请求切换穿透模式
    toggle_ghost_signal = pyqtSignal(bool)
    
    def __init__(self, pet_window, app):
        super().__init__()
        self.pet_window = pet_window
        self.app = app
        
        # 创建托盘图标 (暂时用 idle 图片)
        self.tray_icon = QSystemTrayIcon(self)
        # 尝试获取图标，如果没有就暂时为空
        # loading logic mirrors PetWindow
        if hasattr(pet_window, 'state_images') and len(pet_window.state_images) > 0:
             # Use the first available image
             pixmap = list(pet_window.state_images.values())[0]
             self.tray_icon.setIcon(QIcon(pixmap))
        else:
             self.tray_icon.setIcon(QIcon("assets/icon.png")) # Fallback
             
        self.init_menu()
        self.tray_icon.show()
        
    def init_menu(self):
        menu = QMenu()
        
        # 锁定/穿透模式
        self.ghost_action = QAction("锁定 (鼠标穿透)", self)
        self.ghost_action.setCheckable(True)
        self.ghost_action.setChecked(False)
        self.ghost_action.triggered.connect(self.on_toggle_ghost)
        menu.addAction(self.ghost_action)
        
        menu.addSeparator()
        
        # 还原位置 (防止飞出屏幕)
        reset_pos_action = QAction("重置位置", self)
        reset_pos_action.triggered.connect(self.pet_window.reset_position)
        menu.addAction(reset_pos_action)
        
        menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        
    def on_toggle_ghost(self, checked):
        self.pet_window.set_ghost_mode(checked)
        if checked:
            self.ghost_action.setText("解锁 (恢复交互)")
        else:
            self.ghost_action.setText("锁定 (鼠标穿透)")

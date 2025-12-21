import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.pet_window import PetWindow
from src.logger import logger  # 初始化日志
from src.tray_icon import SystemTray

import signal
import sys

def main():
    logger.info("启动应用程序...")
    app = QApplication(sys.argv)
    
    # 可以在这里做一些全局配置，比如样式表
    
    pet = PetWindow()
    pet.show()

    # 关键：添加一个定时器让 Python解释器 有机会运行，从而能捕获信号
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    # 初始化托盘图标
    tray = SystemTray(pet, app)
    
    # 3. 设置清理逻辑
    def signal_handler(signum, frame):
        logger.info(f"用户强制退出 ({signal.Signals(signum).name})")
        pet.close() # 触发保存
        app.quit() # 退出 Qt 事件循环
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # 正常运行
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

from PyQt6.QtCore import QObject, QTimer
import time
from src.logger import logger
from src.database import db_manager

class ActivityRecorder(QObject):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._record_activity)
        # Record every 60 seconds
        self.interval_ms = 60 * 1000 
        
    def start(self):
        logger.info("启动 ActivityRecorder (每 60 秒记录一次)...")
        self.timer.start(self.interval_ms)
        
    def stop(self):
        logger.info("停止 ActivityRecorder...")
        self.timer.stop()
        # Try to record one last time if there's pending data?
        # Maybe better not to block exit, or just do a quick check.
        self._record_activity()

    def _record_activity(self):
        kb, mouse = self.monitor.pop_accumulated_counts()
        
        # If no activity, maybe skip? 
        # Plan says: "如果 1 分钟内无操作，则不写入（节省空间）。"
        if kb == 0 and mouse == 0:
            return
            
        timestamp = int(time.time())
        try:
            db_manager.insert_activity(timestamp, kb, mouse)
            logger.info(f"已归档活动记录: Time={timestamp}, Keys={kb}, Mouse={mouse}")
        except Exception as e:
            logger.error(f"归档活动记录失败: {e}")

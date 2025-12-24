import sqlite3
import os
from src.logger import logger

DB_FILE = "user_data.db"

class DatabaseManager:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                # Create activity_logs_minute table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS activity_logs_minute (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp INTEGER NOT NULL,
                        keys_count INTEGER DEFAULT 0,
                        mouse_count INTEGER DEFAULT 0
                    )
                """)
                # Create index on timestamp for faster queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON activity_logs_minute (timestamp)
                """)
                conn.commit()
                logger.info("数据库初始化完成: activity_logs_minute")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")

    def insert_activity(self, timestamp: int, keys: int, mouse: int):
        """
        插入一条分钟级活动记录
        """
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO activity_logs_minute (timestamp, keys_count, mouse_count)
                    VALUES (?, ?, ?)
                """, (timestamp, keys, mouse))
                conn.commit()
                # logger.debug(f"已保存活动记录: {timestamp}, K:{keys}, M:{mouse}")
        except Exception as e:
            logger.error(f"保存活动记录失败: {e}")

    def get_activities_by_range(self, start_ts: int, end_ts: int):
        """
        查询指定时间范围内的活动记录
        """
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT timestamp, keys_count, mouse_count 
                    FROM activity_logs_minute 
                    WHERE timestamp >= ? AND timestamp <= ?
                    ORDER BY timestamp ASC
                """, (start_ts, end_ts))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"查询活动记录失败: {e}")
            return []

    def get_aggregated_stats(self, start_ts: int, end_ts: int, group_by: str = 'hour'):
        """
        获取聚合统计数据
        :param group_by: 'hour' or 'day'
        :return: list of tuples (time_key, total_keys, total_mouse, active_minutes)
        """
        valid_groups = {
            'hour': "%H",
            'day': "%Y-%m-%d",
            'date_hour': "%Y-%m-%d %H:00" # specific hour of specific day
        }
        fmt = valid_groups.get(group_by, "%H")
        
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                # 统计: 键总数, 鼠总数, 活跃分钟数(记录条数)
                sql = f"""
                    SELECT 
                        strftime('{fmt}', timestamp, 'unixepoch', 'localtime') as time_bucket,
                        SUM(keys_count), 
                        SUM(mouse_count),
                        COUNT(*)
                    FROM activity_logs_minute 
                    WHERE timestamp >= ? AND timestamp <= ?
                    GROUP BY time_bucket
                    ORDER BY time_bucket ASC
                """
                cursor.execute(sql, (start_ts, end_ts))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"统计查询失败 ({group_by}): {e}")
            return []

# Global instance
db_manager = DatabaseManager()

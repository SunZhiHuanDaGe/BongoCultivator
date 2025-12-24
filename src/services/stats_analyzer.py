from datetime import datetime, timedelta
import time
from src.database import db_manager

class StatsAnalyzer:
    def __init__(self, db=None):
        self.db = db if db else db_manager

    def _get_start_of_day_ts(self, dt=None):
        if dt is None:
            dt = datetime.now()
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return int(start.timestamp())

    def get_today_overview(self):
        """
        获取今日概览
        Returns:
            dict: {
                'total_keys': int,
                'total_mouse': int,
                'active_minutes': int,
                'most_busy_hour': str ('14:00'),
                'hourly_trend': list [24 ints of activity]
            }
        """
        start_ts = self._get_start_of_day_ts()
        end_ts = int(time.time())
        
        # 1. 聚合查询
        # group_by='hour' returns '00', '01', ... '23'
        rows = self.db.get_aggregated_stats(start_ts, end_ts, group_by='hour')
        
        total_keys = 0
        total_mouse = 0
        active_minutes = 0
        trend_map = {}
        
        for r in rows:
            hour_str, k, m, mins = r 
            # hour_str is '00', '14' etc.
            total_keys += k
            total_mouse += m
            active_minutes += mins
            # Store total activity (k+m) for trend
            trend_map[int(hour_str)] = k + m
            
        # Fill 24 chart
        hourly_trend = []
        max_act = -1
        busy_hour_idx = -1
        
        for h in range(24):
            val = trend_map.get(h, 0)
            hourly_trend.append(val)
            if val > max_act:
                max_act = val
                busy_hour_idx = h
                
        busy_hour_str = f"{busy_hour_idx:02d}:00" if max_act > 0 else "-"
        
        return {
            'total_keys': total_keys,
            'total_mouse': total_mouse,
            'active_minutes': active_minutes,
            'most_busy_hour': busy_hour_str,
            'hourly_trend': hourly_trend
        }

    def get_period_stats(self, period_type='week'):
        """
        获取周期统计 (周/月/年)
        period_type: 'week' (Recent 7 days), 'month' (Current Month), 'year' (Recent 12 months? or Current Year?)
        Let's do:
         - week: Past 7 days (including today)
         - month: Current month (from 1st)
         - year: Current year (from Jan 1st)
        """
        now = datetime.now()
        end_ts = int(now.timestamp())
        
        trend = []
        labels = []
        start_ts = 0
        group_fmt = 'day'
        
        if period_type == 'week':
            # Last 6 days + today
            start_dt = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
            start_ts = int(start_dt.timestamp())
            
            # Query grouped by day
            rows = self.db.get_aggregated_stats(start_ts, end_ts, group_by='day')
            # rows: [('2023-10-01', k, m, mins), ...]
            
            # Map results
            data_map = {}
            for r in rows:
                data_map[r[0]] = r[1] + r[2] # Total Action
            
            # Fill last 7 days
            curr = start_dt
            for _ in range(7):
                date_str = curr.strftime("%Y-%m-%d")
                val = data_map.get(date_str, 0)
                trend.append(val)
                labels.append(curr.strftime("%m-%d")) # Label MM-DD
                curr += timedelta(days=1)
                
        elif period_type == 'month':
            # This month (from 1st)
            start_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_ts = int(start_dt.timestamp())
            
            rows = self.db.get_aggregated_stats(start_ts, end_ts, group_by='day')
            data_map = {r[0]: (r[1] + r[2]) for r in rows}
            
            # Iterate from 1st to today
            curr = start_dt
            while curr <= now:
                date_str = curr.strftime("%Y-%m-%d")
                trend.append(data_map.get(date_str, 0))
                labels.append(curr.strftime("%d")) # Label DD
                curr += timedelta(days=1)
                
        elif period_type == 'year':
            # This year (month resolution?) or just day resolution?
            # Year view usually needs Month resolution. 
            # Our DB supports 'day'. We can aggregate 'day' results into months here in python 
            # OR add 'month' support in DB.
            # Let's aggregate here for simplicity if data isn't huge.
            # Actually, let's query raw by day and sum up.
            start_dt = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            start_ts = int(start_dt.timestamp())
            
            rows = self.db.get_aggregated_stats(start_ts, end_ts, group_by='day')
            # Aggregate to months: keys 'YYYY-MM-DD' -> 'MM'
            month_map = {} # '01' -> val
            
            for r in rows:
                d_str = r[0] # YYYY-MM-DD
                month = d_str.split('-')[1]
                val = r[1] + r[2]
                month_map[month] = month_map.get(month, 0) + val
                
            # 1..12
            for m in range(1, 13):
                m_str = f"{m:02d}"
                trend.append(month_map.get(m_str, 0))
                labels.append(m_str)
        
        # Calculate summary from trend
        total_actions = sum(trend)
        
        # Find busiest
        max_val = -1
        busy_idx = -1
        for i, val in enumerate(trend):
            if val > max_val:
                max_val = val
                busy_idx = i
                
        busy_label = labels[busy_idx] if max_val > 0 else "-"
        
        return {
            'total_actions': total_actions,
            'trend': trend,
            'labels': labels,
            'busiest_period': busy_label 
        }

# Global
stats_analyzer = StatsAnalyzer()

import json
import os
import threading
import time
from datetime import datetime, timedelta

STATS_FILE = "data/stats.json"
SAVE_INTERVAL = 900

class StatsManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.stats = self.load_stats()
        self.last_save = time.time()
        self.start_autosave()

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_stats(self):
        with self.lock:
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)

    def start_autosave(self):
        def autosave():
            while True:
                time.sleep(SAVE_INTERVAL)
                self.save_stats()
        t = threading.Thread(target=autosave, daemon=True)
        t.start()

    def _get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _get_week_dates(self):
        today = datetime.now().date()
        return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    def _init_key(self, key):
        if key not in self.stats:
            self.stats[key] = {
                "total": 0,
                "by_day": {}
            }

    def increment(self, key):
        with self.lock:
            self._init_key(key)
            today = self._get_today()
            self.stats[key]["total"] += 1
            self.stats[key]["by_day"].setdefault(today, 0)
            self.stats[key]["by_day"][today] += 1

    def get_stats(self, key):
        self._init_key(key)
        today = self._get_today()
        week_dates = self._get_week_dates()
        by_day = self.stats[key]["by_day"]
        week = sum(by_day.get(day, 0) for day in week_dates)
        today_count = by_day.get(today, 0)
        return {
            "today": today_count,
            "week": week,
            "total": self.stats[key]["total"]
        }

    def cleanup_old_days(self):
        # Call this periodically to remove days older than 7 days
        week_dates = set(self._get_week_dates())
        for key in self.stats:
            by_day = self.stats[key]["by_day"]
            for day in list(by_day.keys()):
                if day not in week_dates:
                    del by_day[day]

stats_manager = StatsManager()

from datetime import datetime
from collections import defaultdict


class ServiceStats:
    def __init__(self):
        self.version = "1.0.0"
        self.started_at = datetime.utcnow()
        self.request_counts = defaultdict(int)
        self.total_requests = 0

    def record_request(self, status_code: int):
        self.total_requests += 1
        self.request_counts[status_code] += 1

    def get_stats(self) -> dict:
        now = datetime.utcnow()
        uptime = (now - self.started_at).total_seconds()
        return {
            "version": self.version,
            "started_at": self.started_at.isoformat(),
            "uptime_seconds": int(uptime),
            "requests": {
                "total": self.total_requests,
                "by_status": dict(self.request_counts),
            },
        }


stats = ServiceStats()
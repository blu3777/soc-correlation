import random
from datetime import datetime, timedelta
import pytz

class EventCollector:
    def __init__(self, timezone):
        self.tz = pytz.timezone(timezone)

    def generate_event(self, timestamp, user, ip, status, event_type):
        return {
            "timestamp": timestamp,
            "user": user,
            "ip": ip,
            "status": status,
            "event_type": event_type
        }

    def generate_dataset(self):
        now = datetime.now(self.tz)

        events = []

        # Usuário normal
        for i in range(3):
            events.append(self.generate_event(
                now.replace(hour=10+i),
                "alice",
                "10.0.0.1",
                "SUCCESS",
                "login"
            ))

        # Usuário suspeito
        base = now.replace(hour=3, minute=30)
        for i in range(3):
            events.append(self.generate_event(
                base + timedelta(minutes=i),
                "john_doe",
                "192.168.1.100",
                "FAIL",
                "login"
            ))

        events.append(self.generate_event(
            base + timedelta(minutes=5),
            "john_doe",
            "192.168.1.100",
            "SUCCESS",
            "login"
        ))

        # Brute force
        for i in range(6):
            events.append(self.generate_event(
                now.replace(hour=14, minute=i),
                "admin",
                f"200.10.0.{i}",
                "FAIL",
                "login"
            ))

        return events


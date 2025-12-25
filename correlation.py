import uuid
from datetime import timedelta

class CorrelationEngine:
    def __init__(self, config):
        self.window = timedelta(
            minutes=config["thresholds"]["correlation_window_minutes"]
        )

    def correlate(self, events):
        events.sort(key=lambda x: x["timestamp"])
        correlated = []

        while events:
            base = events.pop(0)
            group = [base]

            for event in events[:]:
                if (
                    event["user"] == base["user"]
                    and event["ip"] == base["ip"]
                    and event["timestamp"] - base["timestamp"] <= self.window
                ):
                    group.append(event)
                    events.remove(event)

            correlated.append({
                "incident_id": f"INC-{uuid.uuid4()}",
                "events": group
            })

        return correlated
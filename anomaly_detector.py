from datetime import timedelta

class AnomalyDetector:
    def __init__(self, config):
        self.config = config

    def is_anomalous_time(self, event):
        hour = event["timestamp"].hour
        start = self.config["anomalous_hours"]["start"]
        end = self.config["anomalous_hours"]["end"]

        return hour >= start or hour <= end

    def detect_failed_sequence(self, events):
        failures = []
        window = timedelta(minutes=self.config["thresholds"]["failure_window_minutes"])

        for i, event in enumerate(events):
            if event["status"] == "FAIL":
                start_time = event["timestamp"]
                count = 1

                for next_event in events[i+1:]:
                    if next_event["timestamp"] - start_time <= window and next_event["status"] == "FAIL":
                        count += 1

                if count >= self.config["thresholds"]["failed_logins"]:
                    failures.append(event)

        return failures

    def success_after_failures(self, events):
        fail_seen = False
        for event in events:
            if event["status"] == "FAIL":
                fail_seen = True
            if event["status"] == "SUCCESS" and fail_seen:
                return True
        return False
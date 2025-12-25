import json

class IncidentManager:
    def __init__(self, config):
        self.config = config

    def classify(self, incident, detector):
        events = incident["events"]

        failures = [e for e in events if e["status"] == "FAIL"]
        success_after = detector.success_after_failures(events)
        anomalous = any(detector.is_anomalous_time(e) for e in events)

        if failures and success_after and anomalous:
            severity = "HIGH"
        elif failures and success_after:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return severity

    def build_incident(self, incident, severity):
        timestamps = [e["timestamp"] for e in incident["events"]]

        return {
            "incident_id": incident["incident_id"],
            "severity": severity,
            "events": incident["events"],
            "timeline": f"{min(timestamps)} → {max(timestamps)}",
            "summary": self.summary(severity),
            "indicators": list({
                f"user:{e['user']}" for e in incident["events"]
            } | {
                f"ip:{e['ip']}" for e in incident["events"]
            }),
            "status": "OPEN"
        }

    def summary(self, severity):
        return {
            "LOW": "Falhas esporádicas de autenticação",
            "MEDIUM": "Múltiplas falhas seguidas de sucesso",
            "HIGH": "Múltiplas falhas seguidas de sucesso em horário anômalo"
        }[severity]

    def persist(self, incident, path):
        try:
            with open(path, "a") as f:
                f.write(json.dumps(incident, default=str) + "\n")
        except Exception as e:
            print(f"[ERROR] Persistência falhou: {e}")
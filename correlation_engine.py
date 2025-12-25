import yaml
from event_generator import EventCollector
from anomaly_detector import AnomalyDetector
from correlation import CorrelationEngine
from incident_manager import IncidentManager

def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    collector = EventCollector(config["timezone"])
    detector = AnomalyDetector(config)
    correlator = CorrelationEngine(config)
    manager = IncidentManager(config)

    events = collector.generate_dataset()
    incidents = correlator.correlate(events)

    print("\n=== DASHBOARD SOC ===\n")

    for inc in incidents:
        severity = manager.classify(inc, detector)
        incident = manager.build_incident(inc, severity)
        manager.persist(incident, config["persistence"]["incident_file"])

        print(f"[{incident['severity']}] {incident['incident_id']}")
        print(f"Resumo: {incident['summary']}")
        print(f"Indicadores: {incident['indicators']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
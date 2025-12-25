def test_incident_structure(incident):
    required = ["incident_id", "severity", "events", "timeline", "summary"]
    for r in required:
        assert r in incident

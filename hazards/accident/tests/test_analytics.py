import pytest
import json
from hazards.accident.analytics.incident_manager import IncidentManager
from hazards.accident.analytics.severity import calculate_acri
from hazards.accident.analytics.vulnerability import calculate_vulnerability
from hazards.accident.analytics.analyzer import Analyzer
from shared.contracts.detection import Detection
from shared.contracts.accident_event import AccidentEvent


@pytest.fixture
def config():
    return {
        "persistence": {"accident_frames": 2, "pedestrian_hazard_frames": 2},
        "acri_weights": {
            "accident_area": 0.5, "pedestrian_count": 0.5,
            "accident_count": 0.0, "persistence_duration": 0.0, "vehicle_density": 0.0
        },
        "vulnerability_weights": {"pedestrian_count": 1.0, "vehicle_density": 0.0},
        "escalation": {"acri_threshold": 0.70},
        "dark_spot": {"incident_count_threshold": 3}
    }


def test_acri_calculation(config):
    # max accident area + max pedestrian count -> acri = 1.0
    acri = calculate_acri(1.0, 20, 0, 0, 0, config)
    assert acri == 1.0


def test_acri_zero(config):
    acri = calculate_acri(0.0, 0, 0, 0, 0, config)
    assert acri == 0.0


def test_vulnerability_calculation(config):
    vuln = calculate_vulnerability(20, 0, config)
    assert vuln == 1.0


def test_incident_lifecycle_and_escalation(config):
    manager = IncidentManager(config)
    event   = manager.create(0.5, 0.2, 0.1, "collision")
    assert event.status == "active"

    # Push over escalation threshold
    event2 = manager.update(event.incident_id, 0.9, 0.5, 0.5)
    assert event2.status == "escalated"

    # Resolve
    event3 = manager.resolve(event.incident_id)
    assert event3.status == "resolved"

    # Update on resolved should not reopen
    event4 = manager.update(event.incident_id, 0.95, 0.9, 0.9)
    assert event4.status == "resolved"


def test_persistence_logic_collision(config):
    analyzer = Analyzer(config)
    d = Detection(frame_id=1, timestamp=1.0, class_name="accident",
                  confidence=0.9, bbox=[0, 0, 0.2, 0.2])

    # Frame 1: below threshold (threshold is 2)
    e1 = analyzer.process_frame([d])
    assert e1 is None

    # Frame 2: threshold met
    e2 = analyzer.process_frame([d])
    assert e2 is not None
    assert e2.hazard_type == "collision"
    assert e2.status in ("active", "escalated")


def test_persistence_logic_pedestrian(config):
    analyzer = Analyzer(config)
    d = Detection(frame_id=1, timestamp=1.0, class_name="pedestrian_hazard",
                  confidence=0.85, bbox=[0, 0, 0.1, 0.2])

    e1 = analyzer.process_frame([d])
    assert e1 is None

    e2 = analyzer.process_frame([d])
    assert e2 is not None
    assert e2.hazard_type == "pedestrian_hazard"


def test_dark_spot_detection(config):
    manager = IncidentManager(config)
    # 3 incidents at same location should flag dark spot
    for i in range(3):
        event = manager.create(0.5, 0.3, 0.2, "collision", location_id="cam_X")
    assert event.dark_spot is True


def test_schema_validation():
    event = AccidentEvent("abc-123", 1.0, 0.5, 0.4, 0.6, "collision", "active", False)
    json_str = event.to_json()
    parsed   = json.loads(json_str)
    assert parsed["incident_id"] == "abc-123"
    assert parsed["hazard_type"] == "collision"
    assert parsed["dark_spot"] is False

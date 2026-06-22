
import pytest
from hazards.fire.analytics.incident_manager import IncidentManager
from hazards.fire.analytics.severity import calculate_psri
from hazards.fire.analytics.vulnerability import calculate_vulnerability
from hazards.fire.analytics.analyzer import Analyzer
from shared.contracts.detection import Detection
from shared.contracts.fire_event import FireEvent
import json

@pytest.fixture
def config():
    return {
        "persistence": {"fire_frames": 2, "smoke_frames": 3},
        "psri_weights": {
            "fire_area": 0.5, "smoke_area": 0.0, "fire_count": 0.0, 
            "smoke_count": 0.0, "persistence_duration": 0.0, 
            "people_exposure": 0.5, "vehicle_exposure": 0.0
        },
        "vulnerability_weights": {"people_count": 1.0, "vehicle_count": 0.0, "crowd_density": 0.0},
        "escalation": {"psri_threshold": 0.8}
    }

def test_psri_calculation(config):
    # fire area = 1.0 (max), people exposure = 50 (max) -> 0.5 * 1.0 + 0.5 * 1.0 = 1.0
    psri = calculate_psri(1.0, 0.0, 0, 0, 0, 50, 0, config)
    assert psri == 1.0

def test_incident_lifecycle_and_escalation(config):
    manager = IncidentManager(config)
    event = manager.create(0.5, 0.2, 0.1)
    assert event.status == "active"
    
    # Update to trigger escalation (psri >= 0.8)
    event2 = manager.update(event.incident_id, 0.9, 0.5, 0.5)
    assert event2.status == "escalated"
    
    # Resolve
    event3 = manager.resolve(event.incident_id)
    assert event3.status == "resolved"
    
    # Update on resolved does not change status back
    event4 = manager.update(event.incident_id, 0.9, 0.5, 0.5)
    assert event4.status == "resolved"

def test_persistence_logic(config):
    analyzer = Analyzer(config)
    d = Detection(frame_id=1, timestamp=1.0, class_name="fire", confidence=0.9, bbox=[0,0,0.1,0.1])
    
    # Frame 1: no incident (threshold is 2)
    e1 = analyzer.process_frame([d])
    assert e1 is None
    
    # Frame 2: threshold met
    e2 = analyzer.process_frame([d])
    assert e2 is not None
    assert e2.incident_id is not None
    assert e2.status == "active"

def test_schema_validation():
    event = FireEvent("123", 1.0, 0.5, 0.5, 0.5, "fire", "active")
    json_str = event.to_json()
    parsed = json.loads(json_str)
    assert parsed["incident_id"] == "123"
    assert parsed["status"] == "active"

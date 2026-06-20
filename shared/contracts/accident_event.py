from dataclasses import dataclass, asdict
import json

@dataclass
class AccidentEvent:
    incident_id: str
    timestamp: float
    severity_score: float
    vulnerability_score: float
    acri_score: float
    hazard_type: str   # "collision" or "pedestrian_hazard"
    status: str        # "active", "escalated", "resolved"
    dark_spot: bool    # True if this location has repeated incidents

    def to_json(self):
        return json.dumps(asdict(self))

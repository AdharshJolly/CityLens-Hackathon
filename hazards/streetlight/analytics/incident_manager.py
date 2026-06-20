import uuid
import time
from shared.contracts.streetlight_event import StreetlightEvent

class IncidentManager:
    def __init__(self, config):
        self.config = config
        self.incidents = {}
        self.escalation_threshold = 0.75

    def create(self, severity, brightness, flicker):
        incident_id = str(uuid.uuid4())

        event = StreetlightEvent(
            incident_id=incident_id,
            timestamp=time.time(),
            severity_score=severity,
            brightness_score=brightness,
            flicker_score=flicker,
            hazard_type="streetlight",
            status="escalated" if severity >= self.escalation_threshold else "active"
        )

        self.incidents[incident_id] = event
        return event

    def update(self, incident_id, severity, brightness, flicker):
        if incident_id in self.incidents:
            event = self.incidents[incident_id]

            if event.status == "resolved":
                return event

            event.severity_score = severity
            event.brightness_score = brightness
            event.flicker_score = flicker

            if severity >= self.escalation_threshold:
                event.status = "escalated"

            return event
        return None

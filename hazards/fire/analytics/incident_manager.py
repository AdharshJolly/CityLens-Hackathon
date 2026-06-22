
import uuid
import time
from shared.contracts.fire_event import FireEvent

class IncidentManager:
    def __init__(self, config):
        self.config = config
        self.incidents = {}
        self.escalation_threshold = self.config.get("escalation", {}).get("psri_threshold", 0.75)

    def create(self, psri, severity, vulnerability):
        incident_id = str(uuid.uuid4())
        event = FireEvent(
            incident_id=incident_id,
            timestamp=time.time(),
            severity_score=severity,
            vulnerability_score=vulnerability,
            psri_score=psri,
            hazard_type="fire",
            status="escalated" if psri >= self.escalation_threshold else "active"
        )
        self.incidents[incident_id] = event
        return event

    def update(self, incident_id, psri, severity, vulnerability):
        if incident_id in self.incidents:
            event = self.incidents[incident_id]
            if event.status == "resolved":
                return event
                
            event.severity_score = severity
            event.vulnerability_score = vulnerability
            event.psri_score = psri
            
            if psri >= self.escalation_threshold and event.status == "active":
                event.status = "escalated"
                
            return event
        return None

    def escalate(self, incident_id):
        if incident_id in self.incidents:
            event = self.incidents[incident_id]
            if event.status == "active":
                event.status = "escalated"
            return event
        return None

    def resolve(self, incident_id):
        if incident_id in self.incidents:
            event = self.incidents[incident_id]
            event.status = "resolved"
            return event
        return None

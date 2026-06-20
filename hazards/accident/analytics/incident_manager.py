import uuid
import time
from shared.contracts.accident_event import AccidentEvent


class IncidentManager:
    def __init__(self, config):
        self.config = config
        self.incidents = {}
        self.location_incident_counts = {}  # tracks repeated incidents per camera/location

        self.escalation_threshold = self.config.get("escalation", {}).get("acri_threshold", 0.70)
        self.dark_spot_threshold  = self.config.get("dark_spot", {}).get("incident_count_threshold", 3)

    def create(self, acri, severity, vulnerability, hazard_type, location_id="default"):
        incident_id = str(uuid.uuid4())

        # Increment incident count for this location (dark spot logic)
        self.location_incident_counts[location_id] = \
            self.location_incident_counts.get(location_id, 0) + 1
        is_dark_spot = self.location_incident_counts[location_id] >= self.dark_spot_threshold

        event = AccidentEvent(
            incident_id=incident_id,
            timestamp=time.time(),
            severity_score=severity,
            vulnerability_score=vulnerability,
            acri_score=acri,
            hazard_type=hazard_type,
            status="escalated" if acri >= self.escalation_threshold else "active",
            dark_spot=is_dark_spot
        )
        self.incidents[incident_id] = event
        return event

    def update(self, incident_id, acri, severity, vulnerability):
        if incident_id not in self.incidents:
            return None

        event = self.incidents[incident_id]
        if event.status == "resolved":
            return event

        event.severity_score     = severity
        event.vulnerability_score = vulnerability
        event.acri_score          = acri

        if acri >= self.escalation_threshold and event.status == "active":
            event.status = "escalated"

        return event

    def escalate(self, incident_id):
        if incident_id in self.incidents:
            event = self.incidents[incident_id]
            if event.status == "active":
                event.status = "escalated"
            return event
        return None

    def resolve(self, incident_id):
        if incident_id in self.incidents:
            self.incidents[incident_id].status = "resolved"
        return self.incidents.get(incident_id)

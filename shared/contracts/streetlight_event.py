class StreetlightEvent:
    def __init__(
        self,
        incident_id,
        timestamp,
        severity_score,
        brightness_score,
        flicker_score,
        hazard_type,
        status
    ):
        self.incident_id = incident_id
        self.timestamp = timestamp
        self.severity_score = severity_score
        self.brightness_score = brightness_score
        self.flicker_score = flicker_score
        self.hazard_type = hazard_type
        self.status = status

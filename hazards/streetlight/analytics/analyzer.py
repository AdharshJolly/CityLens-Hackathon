from hazards.streetlight.analytics.severity import calculate_severity
from hazards.streetlight.analytics.incident_manager import IncidentManager
from hazards.streetlight.analytics.brightness import calculate_brightness


class Analyzer:
    def __init__(self, config):
        self.config = config
        self.manager = IncidentManager(config)
        self.active_incident_id = None

        self.consecutive_off_frames = 0
        self.previous_brightness = None

    def process_frame(self, frame, detections):
        if not detections:
            return None

        detection = detections[0]
        brightness = calculate_brightness(frame, detection.bbox)

        # OFF state detection
        if brightness < 0.3:
            self.consecutive_off_frames += 1
        else:
            self.consecutive_off_frames = 0

        # Flicker detection
        flicker_score = 0
        if self.previous_brightness is not None:
            diff = abs(brightness - self.previous_brightness)

            if diff > 0.4:
                flicker_score = 1

        self.previous_brightness = brightness

        # Ignore if no real issue
        if self.consecutive_off_frames < 3 and flicker_score == 0:
            return None

        severity = calculate_severity(
            brightness,
            flicker_score,
            self.config
        )

        if self.active_incident_id is None:
            event = self.manager.create(
                severity,
                brightness,
                flicker_score
            )
            self.active_incident_id = event.incident_id
            return event

        return self.manager.update(
            self.active_incident_id,
            severity,
            brightness,
            flicker_score
        )

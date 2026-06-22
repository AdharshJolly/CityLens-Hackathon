from typing import List
from shared.contracts.detection import Detection
from hazards.accident.analytics.severity import calculate_acri
from hazards.accident.analytics.vulnerability import calculate_vulnerability
from hazards.accident.analytics.incident_manager import IncidentManager


class Analyzer:
    def __init__(self, config):
        self.config   = config
        self.manager  = IncidentManager(config)
        self.active_incident_id = None

        # Persistence counters — hazard must appear for N consecutive frames before triggering
        self.consecutive_accident_frames   = 0
        self.consecutive_pedestrian_frames = 0

        self.accident_threshold   = self.config.get("persistence", {}).get("accident_frames", 3)
        self.pedestrian_threshold = self.config.get("persistence", {}).get("pedestrian_hazard_frames", 2)

    def process_frame(self, detections: List[Detection],
                      pedestrian_count=0, vehicle_count=0, location_id="default"):
        """
        Called once per video frame.
        Returns an AccidentEvent if an incident is active, else None.
        """
        accident_dets   = [d for d in detections if d.class_name == "accident"]
        pedestrian_dets = [d for d in detections if d.class_name == "pedestrian_hazard"]

        # Update persistence counters
        self.consecutive_accident_frames   = (self.consecutive_accident_frames + 1) \
                                              if accident_dets else 0
        self.consecutive_pedestrian_frames = (self.consecutive_pedestrian_frames + 1) \
                                              if pedestrian_dets else 0

        accident_triggered   = self.consecutive_accident_frames   >= self.accident_threshold
        pedestrian_triggered = self.consecutive_pedestrian_frames >= self.pedestrian_threshold

        if not accident_triggered and not pedestrian_triggered:
            return None

        # Determine primary hazard type for this event
        hazard_type = "collision" if accident_triggered else "pedestrian_hazard"

        # Calculate bounding box area coverage
        accident_area = sum(d.bbox[2] * d.bbox[3] for d in accident_dets)
        persistence   = max(self.consecutive_accident_frames, self.consecutive_pedestrian_frames)

        acri  = calculate_acri(accident_area, pedestrian_count, len(accident_dets),
                               persistence, vehicle_count, self.config)
        vuln  = calculate_vulnerability(pedestrian_count, vehicle_count, self.config)
        sev   = min(1.0, accident_area)  # severity = how much of the frame is affected

        if self.active_incident_id is None:
            event = self.manager.create(acri, sev, vuln, hazard_type, location_id)
            self.active_incident_id = event.incident_id
        else:
            event = self.manager.update(self.active_incident_id, acri, sev, vuln)

        return event

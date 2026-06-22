
from typing import List
from shared.contracts.detection import Detection
from hazards.fire.analytics.severity import calculate_psri
from hazards.fire.analytics.vulnerability import calculate_vulnerability
from hazards.fire.analytics.incident_manager import IncidentManager

class Analyzer:
    def __init__(self, config):
        self.config = config
        self.manager = IncidentManager(config)
        self.active_incident_id = None
        
        # Persistence tracking
        self.consecutive_fire_frames = 0
        self.consecutive_smoke_frames = 0
        self.fire_threshold = self.config.get("persistence", {}).get("fire_frames", 3)
        self.smoke_threshold = self.config.get("persistence", {}).get("smoke_frames", 5)

    def process_frame(self, detections: List[Detection], people_count=0, vehicle_count=0):
        fire_dets = [d for d in detections if d.class_name == "fire"]
        smoke_dets = [d for d in detections if d.class_name == "smoke"]
        
        # Calculate Areas (assuming bbox is normalized 0-1)
        fire_area = sum(d.bbox[2]*d.bbox[3] for d in fire_dets)
        smoke_area = sum(d.bbox[2]*d.bbox[3] for d in smoke_dets)
        
        # Persistence logic
        if fire_dets:
            self.consecutive_fire_frames += 1
        else:
            self.consecutive_fire_frames = 0
            
        if smoke_dets:
            self.consecutive_smoke_frames += 1
        else:
            self.consecutive_smoke_frames = 0

        # Check if thresholds met
        hazard_detected = (self.consecutive_fire_frames >= self.fire_threshold) or (self.consecutive_smoke_frames >= self.smoke_threshold)
        
        if not hazard_detected:
            # If no hazard and we have an incident, we could resolve it, but let's keep it simple
            return None

        # Calculate scores
        vuln_score = calculate_vulnerability(people_count, vehicle_count, 0.0, self.config)
        
        persistence_duration = max(self.consecutive_fire_frames, self.consecutive_smoke_frames)
        
        psri_score = calculate_psri(
            fire_area=fire_area,
            smoke_area=smoke_area,
            fire_count=len(fire_dets),
            smoke_count=len(smoke_dets),
            persistence_duration=persistence_duration,
            people_exposure=people_count,
            vehicle_exposure=vehicle_count,
            config=self.config
        )
        
        # We assume severity is just raw fire/smoke impact for legacy, but we use PSRI for everything
        sev_score = (fire_area + smoke_area) / 2.0
        
        if self.active_incident_id is None:
            event = self.manager.create(psri_score, sev_score, vuln_score)
            self.active_incident_id = event.incident_id
            return event
        else:
            return self.manager.update(self.active_incident_id, psri_score, sev_score, vuln_score)

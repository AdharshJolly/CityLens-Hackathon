import os
import sys
import json
import random

sys.path.append(os.path.abspath('.'))

from hazards.fire.analytics.analyzer import Analyzer

def generate_mock_detections():
    # Helper to fake ultralytics boxes
    class MockDet:
        def __init__(self, c_name, bbox):
            self.class_name = c_name
            self.bbox = bbox # [x_min, y_min, w_norm, h_norm] -> for area calculation we use w, h
    
    # 0 to 3 fires
    dets = []
    num_fires = random.randint(0, 3)
    num_smoke = random.randint(0, 2)
    
    for _ in range(num_fires):
        dets.append(MockDet("fire", [0.1, 0.1, random.uniform(0.01, 0.2), random.uniform(0.01, 0.2)]))
    for _ in range(num_smoke):
        dets.append(MockDet("smoke", [0.1, 0.1, random.uniform(0.05, 0.4), random.uniform(0.05, 0.4)]))
    return dets

def main():
    print("Generating Analytics Showcase...")
    os.makedirs("outputs/showcase", exist_ok=True)
    
    config = {
        "persistence": {"fire_frames": 1, "smoke_frames": 1},
        "weights": {"severity": 0.4, "vulnerability": 0.3, "exposure": 0.3}
    }
    
    with open("docs/ANALYTICS_SHOWCASE.md", "w") as md:
        md.write("# ANALYTICS SHOWCASE\n\n")
        md.write("This document showcases the PSRI scoring and Vulnerability engines operating on simulated incidents.\n\n")
        
        for i in range(1, 11):
            analyzer = Analyzer(config)
            # simulate 3 frames of persistence
            for _ in range(3):
                dets = generate_mock_detections()
                people = random.randint(0, 5)
                vehicles = random.randint(0, 2)
                event = analyzer.process_frame(dets, people_count=people, vehicle_count=vehicles)
            
            if event:
                event_dict = {
                    "incident_id": event.incident_id,
                    "timestamp": str(event.timestamp),
                    "psri_score": event.psri_score,
                    "severity": event.severity_score,
                    "vulnerability": event.vulnerability_score,
                    "status": getattr(event, "status", "active")
                }
                
                json_path = f"outputs/showcase/incident_{i:02d}.json"
                with open(json_path, "w") as jf:
                    json.dump(event_dict, jf, indent=2)
                
                md.write(f"## Incident {i:02d}\n")
                md.write(f"**ID:** {event.incident_id}\n")
                md.write(f"**PSRI Score:** {event.psri_score:.2f}\n")
                md.write(f"**Vulnerability:** {event.vulnerability_score:.2f}\n")
                md.write(f"**JSON Export:** `outputs/showcase/incident_{i:02d}.json`\n\n")
                
    print("Finished generating showcase.")

if __name__ == "__main__":
    main()

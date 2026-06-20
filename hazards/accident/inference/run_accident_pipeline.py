import sys
import os
import json
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from shared.contracts.detection import Detection
from hazards.accident.analytics.analyzer import Analyzer
from shared.utilities.config_loader import load_config


def generate_sample_outputs():
    config_path = Path(__file__).parent.parent / "configs/thresholds.yaml"
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        return

    config = load_config(str(config_path))

    # ---------------------------------------------------------------
    # SCENARIO 1: Vehicle Collision (3 consecutive frames trigger it)
    # ---------------------------------------------------------------
    print("--- Scenario 1: Vehicle Collision ---")
    analyzer = Analyzer(config)

    d1 = Detection(frame_id=1, timestamp=1.0, class_name="accident", confidence=0.82, bbox=[0.5, 0.5, 0.15, 0.15])
    e1 = analyzer.process_frame([d1], vehicle_count=4, location_id="cam_001")
    print(f"Frame 1 (accident frames: 1): {e1}")

    d2 = Detection(frame_id=2, timestamp=2.0, class_name="accident", confidence=0.85, bbox=[0.5, 0.5, 0.20, 0.20])
    e2 = analyzer.process_frame([d2], vehicle_count=4, location_id="cam_001")
    print(f"Frame 2 (accident frames: 2): {e2}")

    d3 = Detection(frame_id=3, timestamp=3.0, class_name="accident", confidence=0.91, bbox=[0.5, 0.5, 0.55, 0.55])
    e3 = analyzer.process_frame([d3], vehicle_count=6, location_id="cam_001")
    print(f"Frame 3 (threshold hit!) -> Incident:")
    print(e3.to_json())

    d4 = Detection(frame_id=4, timestamp=4.0, class_name="accident", confidence=0.95, bbox=[0.5, 0.5, 0.80, 0.80])
    e4 = analyzer.process_frame([d4, d4, d4], vehicle_count=8, pedestrian_count=5, location_id="cam_001")
    print(f"Frame 4 (escalation):")
    print(e4.to_json())

    # ---------------------------------------------------------------
    # SCENARIO 2: Pedestrian Hazard (2 consecutive frames trigger it)
    # ---------------------------------------------------------------
    print("\n--- Scenario 2: Pedestrian Hazard ---")
    analyzer2 = Analyzer(config)

    p1 = Detection(frame_id=1, timestamp=5.0, class_name="pedestrian_hazard", confidence=0.78, bbox=[0.4, 0.6, 0.10, 0.20])
    ep1 = analyzer2.process_frame([p1], pedestrian_count=6, vehicle_count=3, location_id="cam_002")
    print(f"Frame 1 (pedestrian frames: 1): {ep1}")

    p2 = Detection(frame_id=2, timestamp=6.0, class_name="pedestrian_hazard", confidence=0.83, bbox=[0.4, 0.6, 0.12, 0.22])
    ep2 = analyzer2.process_frame([p2], pedestrian_count=8, vehicle_count=3, location_id="cam_002")
    print(f"Frame 2 (threshold hit!) -> Incident:")
    print(ep2.to_json())

    # ---------------------------------------------------------------
    # SCENARIO 3: Dark Spot — same location triggers 3+ incidents
    # ---------------------------------------------------------------
    print("\n--- Scenario 3: Dark Spot Detection ---")
    analyzer3 = Analyzer(config)
    for i in range(1, 10):
        d = Detection(frame_id=i, timestamp=float(i), class_name="accident",
                      confidence=0.88, bbox=[0.5, 0.5, 0.4, 0.4])
        event = analyzer3.process_frame([d], vehicle_count=5, location_id="cam_003")
        if event:
            print(f"Incident at frame {i}: dark_spot={event.dark_spot} | status={event.status}")
            analyzer3.active_incident_id = None  # reset to force new incident

    # ---------------------------------------------------------------
    # Write sample JSON to output
    # ---------------------------------------------------------------
    out_dir = Path(__file__).parent.parent.parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    if e4:
        with open(out_dir / "sample_accident_event.json", "w") as f:
            f.write(e4.to_json())
        print(f"\nSample JSON saved to outputs/sample_accident_event.json")


if __name__ == "__main__":
    generate_sample_outputs()


import sys
import os
import yaml
from pathlib import Path

# Add project root to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from shared.contracts.detection import Detection
from hazards.fire.analytics.analyzer import Analyzer
from shared.utilities.config_loader import load_config

def generate_sample_outputs():
    config_path = Path(__file__).parent.parent / "configs/thresholds.yaml"
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        return
        
    config = load_config(str(config_path))
    analyzer = Analyzer(config)
    
    print("--- Simulating YOLO Detections ---")
    
    # Frame 1: 1 small fire
    d1 = Detection(frame_id=1, timestamp=1.0, class_name="fire", confidence=0.8, bbox=[0.5, 0.5, 0.1, 0.1])
    e1 = analyzer.process_frame([d1])
    print(f"Frame 1 (Fire frames: 1): Incident -> {e1}")
    
    # Frame 2: 1 small fire
    d2 = Detection(frame_id=2, timestamp=2.0, class_name="fire", confidence=0.8, bbox=[0.5, 0.5, 0.1, 0.1])
    e2 = analyzer.process_frame([d2])
    print(f"Frame 2 (Fire frames: 2): Incident -> {e2}")
    
    # Frame 3: Threshold hit! 1 big fire
    d3 = Detection(frame_id=3, timestamp=3.0, class_name="fire", confidence=0.9, bbox=[0.5, 0.5, 0.8, 0.8])
    e3 = analyzer.process_frame([d3], people_count=10)
    print(f"Frame 3 (Fire frames: 3): Threshold Hit! Incident ->")
    print(e3.to_json())
    
    # Frame 4: Massive fire, escalation
    d4 = Detection(frame_id=4, timestamp=4.0, class_name="fire", confidence=0.95, bbox=[0.5, 0.5, 0.9, 0.9])
    e4 = analyzer.process_frame([d4, d4, d4, d4], people_count=50, vehicle_count=20)
    print(f"Frame 4 (Escalation Phase): Incident ->")
    print(e4.to_json())
    
    # Write sample JSON
    out_dir = Path(__file__).parent.parent.parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "sample_fire_event.json", "w") as f:
        f.write(e4.to_json())
    print(f"\nSample JSON saved to outputs/sample_fire_event.json")

if __name__ == "__main__":
    generate_sample_outputs()

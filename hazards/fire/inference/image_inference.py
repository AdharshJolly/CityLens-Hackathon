
import cv2
import time
from pathlib import Path
from ultralytics import YOLO
from hazards.fire.inference.yolo_adapter import YOLOAdapter
from hazards.fire.analytics.analyzer import Analyzer
from shared.utilities.config_loader import load_config

def draw_overlay(frame, detections, event):
    h, w, _ = frame.shape
    for d in detections:
        x_center, y_center, width, height = d.bbox
        x1 = int((x_center - width/2) * w)
        y1 = int((y_center - height/2) * h)
        x2 = int((x_center + width/2) * w)
        y2 = int((y_center + height/2) * h)
        
        color = (0, 0, 255) if d.class_name == "fire" else (255, 0, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{d.class_name} {d.confidence:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    if event:
        cv2.putText(frame, f"INCIDENT: {event.incident_id[:8]} | {event.status.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"PSRI: {event.psri_score:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return frame

def infer_image(image_path, model_path):
    model = YOLO(model_path)
    adapter = YOLOAdapter()
    
    # Load thresholds correctly assuming script is run from project root
    config_path = Path("hazards/fire/configs/thresholds.yaml")
    if not config_path.exists():
        # fallback for relative path if running directly
        config_path = Path(__file__).parent.parent / "configs/thresholds.yaml"
        
    config = load_config(str(config_path))
    
    # OVERRIDE: For single image demo, drop persistence threshold to 0 so we trigger immediately
    config["persistence"]["fire_frames"] = 0
    config["persistence"]["smoke_frames"] = 0
    
    analyzer = Analyzer(config)
    
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error reading {image_path}")
        return
        
    results = model(frame, verbose=False)
    detections = adapter.adapt(results, frame_id=1, timestamp=time.time())
    
    event = analyzer.process_frame(detections)
    
    frame = draw_overlay(frame, detections, event)
    
    if event:
        out_dir = Path("outputs/incidents")
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / f"{event.incident_id}.json", "w") as f:
            f.write(event.to_json())
            
    out_path = Path("outputs") / "demo_output.jpg"
    out_path.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(out_path), frame)
    return event

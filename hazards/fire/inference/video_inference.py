
import cv2
import time
from pathlib import Path
from ultralytics import YOLO
from hazards.fire.inference.yolo_adapter import YOLOAdapter
from hazards.fire.analytics.analyzer import Analyzer
from shared.utilities.config_loader import load_config
from hazards.fire.inference.image_inference import draw_overlay

def infer_video(video_path, model_path, output_path="outputs/demo_video.mp4"):
    model = YOLO(model_path)
    adapter = YOLOAdapter()
    config = load_config(str(Path("hazards/fire/configs/thresholds.yaml")))
    analyzer = Analyzer(config)
    
    cap = cv2.VideoCapture(video_path)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    
    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame_id += 1
        
        results = model(frame, verbose=False)
        detections = adapter.adapt(results, frame_id=frame_id, timestamp=time.time())
        event = analyzer.process_frame(detections)
        
        frame = draw_overlay(frame, detections, event)
        out.write(frame)
        
        if event:
            out_dir = Path("outputs/incidents")
            out_dir.mkdir(parents=True, exist_ok=True)
            with open(out_dir / f"{event.incident_id}.json", "w") as f:
                f.write(event.to_json())
                
    cap.release()
    out.release()

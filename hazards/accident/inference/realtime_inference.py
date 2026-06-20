import cv2
import time
from pathlib import Path
from ultralytics import YOLO
from hazards.accident.inference.yolo_adapter import YOLOAdapter
from hazards.accident.analytics.analyzer import Analyzer
from hazards.accident.inference.image_inference import draw_overlay
from shared.utilities.config_loader import load_config


def infer_realtime(model_path, camera_index=0, location_id="cam_live"):
    """
    Runs the accident detection pipeline on a live webcam or CCTV feed.
    Press 'q' to quit.
    """
    model    = YOLO(model_path)
    adapter  = YOLOAdapter()
    config   = load_config(str(Path("hazards/accident/configs/thresholds.yaml")))
    analyzer = Analyzer(config)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Cannot open camera at index {camera_index}")
        return

    print("Realtime inference running. Press 'q' to quit.")
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        results    = model(frame, verbose=False)
        detections = adapter.adapt(results, frame_id=frame_id, timestamp=time.time())
        event      = analyzer.process_frame(detections, location_id=location_id)

        frame = draw_overlay(frame, detections, event)
        cv2.imshow("CityShield — Accident Intelligence", frame)

        if event:
            out_dir = Path("outputs/incidents")
            out_dir.mkdir(parents=True, exist_ok=True)
            with open(out_dir / f"{event.incident_id}.json", "w") as f:
                f.write(event.to_json())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

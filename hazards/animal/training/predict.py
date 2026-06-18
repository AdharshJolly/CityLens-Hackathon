from ultralytics import YOLO
import csv
import cv2
import os
from pathlib import Path

# === CONFIG ===
WEIGHTS     = "../../../runs/animal_detection/weights/best.pt"
VALID_IMGS  = "../../../data/animal/valid/images"
OUTPUT_DIR  = "../../../runs/animal_detection/sample_outputs"
RESULTS_CSV = "../../../runs/animal_detection/results.csv"
CONF_THRESH = 0.25
NUM_SAMPLES = 10   # submission requires exactly 10


def run():
    weights_path = Path(WEIGHTS)
    if not weights_path.exists():
        raise FileNotFoundError(f"Weights not found: {weights_path.resolve()}. Run train.py first.")
    
    model = YOLO(str(weights_path))
    
    img_paths = list(Path(VALID_IMGS).glob("*.[jp][pn]g"))
    if len(img_paths) < NUM_SAMPLES:
        print(f"Warning: only {len(img_paths)} validation images found, need {NUM_SAMPLES}")
    samples = img_paths[:NUM_SAMPLES]
    
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    csv_rows = []
    
    for img_path in samples:
        results = model.predict(
            source=str(img_path),
            conf=CONF_THRESH,
            save=False,
            verbose=False
        )
        
        img = cv2.imread(str(img_path))
        result = results[0]
        
        detections = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf   = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            label = f"animal {conf:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            detections.append({
                "image": img_path.name,
                "class": "animal",
                "confidence": round(conf, 4),
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "animal_present": True,
            })
        
        if not detections:
            detections.append({
                "image": img_path.name,
                "class": "none",
                "confidence": 0,
                "x1": 0, "y1": 0, "x2": 0, "y2": 0,
                "animal_present": False,
            })
        
        csv_rows.extend(detections)
        
        out_path = Path(OUTPUT_DIR) / img_path.name
        cv2.imwrite(str(out_path), img)
        print(f"Saved: {out_path.name}  |  detections: {len(result.boxes)}")
    
    # Write CSV
    fieldnames = ["image", "class", "confidence", "x1", "y1", "x2", "y2", "animal_present"]
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"\nresults.csv saved: {Path(RESULTS_CSV).resolve()}")
    print(f"Sample images saved in: {Path(OUTPUT_DIR).resolve()}")


if __name__ == "__main__":
    run()
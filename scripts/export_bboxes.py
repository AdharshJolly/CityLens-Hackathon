import os
import glob
import pandas as pd
from ultralytics import YOLO

# Configuration
MODEL_PATH = "runs/detect/runs/detect/experiments/E003A/weights/best.pt"
TEST_IMAGES_DIR = "data/processed/fire_v3/test/images"
SUBMISSION_DIR = "submission"
OUTPUT_CSV = os.path.join(SUBMISSION_DIR, "predictions.csv")

def main():
    print("Exporting test set bounding boxes...")
    os.makedirs(SUBMISSION_DIR, exist_ok=True)
    
    model = YOLO(MODEL_PATH)
    image_paths = glob.glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))
    
    if not image_paths:
        print(f"Warning: No test images found in {TEST_IMAGES_DIR}")
        return

    all_preds = []
    
    for idx, img_path in enumerate(image_paths):
        img_name = os.path.basename(img_path)
        results = model(img_path, conf=0.25, verbose=False)
        
        for result in results:
            boxes = result.boxes
            for i in range(len(boxes)):
                cls_id = int(boxes.cls[i].item())
                conf = boxes.conf[i].item()
                # Absolute coordinates
                x1, y1, x2, y2 = boxes.xyxy[i].tolist()
                
                all_preds.append({
                    "image_id": img_name,
                    "class_id": cls_id,
                    "confidence": conf,
                    "xmin": x1,
                    "ymin": y1,
                    "xmax": x2,
                    "ymax": y2
                })
        
        if idx % 50 == 0:
            print(f"Processed {idx}/{len(image_paths)} images")
            
    df = pd.DataFrame(all_preds)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Successfully exported {len(all_preds)} predictions to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

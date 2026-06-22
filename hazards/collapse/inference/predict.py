from ultralytics import YOLO
import os
import csv

def run_inference():
    # Load your trained model
    model = YOLO("runs/detect/runs/collapse_v1/weights/best.pt")

    # Input and output folders
    input_dir = "data/collapse/test/images"
    output_dir = "outputs/collapse"
    os.makedirs(output_dir, exist_ok=True)

    # Pick 10 images from test set
    images = os.listdir(input_dir)[:10]

    results_log = []

    for img_name in images:
        img_path = os.path.join(input_dir, img_name)
        results = model(img_path)

        for r in results:
            # Save image with bounding boxes drawn
            annotated = r.plot()
            import cv2
            cv2.imwrite(os.path.join(output_dir, f"out_{img_name}"), annotated)

            # Log bounding boxes to CSV
            for box in r.boxes:
                x, y, w, h = box.xywh[0].tolist()
                conf = float(box.conf)
                cls = int(box.cls)
                results_log.append({
                    "image": img_name,
                    "class": model.names[cls],
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "w": round(w, 2),
                    "h": round(h, 2),
                    "confidence": round(conf, 3)
                })

    # Save CSV
    csv_path = os.path.join(output_dir, "predictions.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image","class","x","y","w","h","confidence"])
        writer.writeheader()
        writer.writerows(results_log)

    print(f"Done! Output saved to: {output_dir}")
    print(f"Images: 10 annotated frames")
    print(f"CSV: {csv_path}")

if __name__ == "__main__":
    run_inference()
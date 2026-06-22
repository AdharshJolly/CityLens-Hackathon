from ultralytics import YOLO
import os
import cv2

def test_real_world():
    model = YOLO("runs/detect/runs/collapse_v1/weights/best.pt")

    input_dir = "data/collapse/real_world_test"
    output_dir = "outputs/collapse/real_world_results"
    os.makedirs(output_dir, exist_ok=True)

    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)
        results = model(img_path, conf=0.25)  # lower confidence threshold to see borderline cases

        for r in results:
            annotated = r.plot()
            cv2.imwrite(os.path.join(output_dir, f"real_{img_name}"), annotated)

            num_detections = len(r.boxes)
            print(f"{img_name}: {num_detections} detections")

if __name__ == "__main__":
    test_real_world()
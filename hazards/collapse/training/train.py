from ultralytics import YOLO
import os

def train():
    model = YOLO("yolo11n.pt")

    results = model.train(
        data=os.path.abspath("hazards/collapse/data/dataset.yaml"),
        epochs=150,          # was 100, more epochs = better convergence
        imgsz=640,
        batch=8,
        project="runs",
        name="collapse_v2",  # new name so v1 is preserved
        save=True,
        plots=True,
        device=0,
        optimizer="AdamW",   # better than default SGD for small models
        lr0=0.001,           # learning rate
        patience=30,         # stop early if no improvement for 30 epochs
        augment=True,        # enable augmentation
        mosaic=1.0,          # mosaic augmentation helps recall
        flipud=0.3,          # vertical flip (trees fall in different directions)
        fliplr=0.5,          # horizontal flip
        degrees=10.0,        # slight rotation
    )

    print("Training complete!")
    print(f"Best weights: runs/collapse_v2/weights/best.pt")

if __name__ == "__main__":
    train()
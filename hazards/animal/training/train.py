from ultralytics import YOLO
import yaml
from pathlib import Path

# === CONFIG ===
MODEL_BASE   = "yolo11n.pt"          # base weights (auto-downloaded first run)
DATASET_YAML = "../../../data/animal/dataset.yaml"
EXPERIMENT   = "animal_detection"
EPOCHS       = 100
BATCH        = 8                     # lower if you hit OOM on 4GB VRAM
IMG_SIZE     = 640
DEVICE       = 0                     # 0 = first GPU; "cpu" if no GPU


def main():
    # Verify dataset.yaml exists
    yaml_path = Path(DATASET_YAML)
    if not yaml_path.exists():
        raise FileNotFoundError(f"dataset.yaml not found at {yaml_path.resolve()}")
    
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f)
    print(f"Dataset config loaded. Classes: {cfg['names']}")
    
    model = YOLO(MODEL_BASE)
    
    results = model.train(
        data      = str(yaml_path),
        epochs    = EPOCHS,
        batch     = BATCH,
        imgsz     = IMG_SIZE,
        device    = DEVICE,
        project   = "../../../runs",
        name      = EXPERIMENT,
        exist_ok  = True,
        patience  = 20,              # early stopping
        save      = True,
        plots     = True,            # generates PR curves, confusion matrix
        verbose   = True,
    )
    
    print("\nTraining complete.")
    best = Path("../../../runs") / EXPERIMENT / "weights" / "best.pt"
    print(f"Best weights: {best.resolve()}")


if __name__ == "__main__":
    main()
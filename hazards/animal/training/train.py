from ultralytics import YOLO
import yaml
from pathlib import Path

MODEL_BASE   = "yolo11n.pt"
BASE         = Path(__file__).resolve().parent.parent
DATASET_YAML = BASE / "data" / "dataset.yaml"
EXPERIMENT   = "animal_detection"
EPOCHS       = 50
BATCH        = 16
IMG_SIZE     = 640
DEVICE       = "cpu"  # 0 = GPU, 'cpu' for CPU

def main():
    yaml_path = Path(DATASET_YAML)
    if not yaml_path.exists():
        raise FileNotFoundError(f"dataset.yaml not found at {yaml_path.resolve()}")
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f)
    print(f"Dataset config loaded. Classes: {cfg['names']}")

    model = YOLO(MODEL_BASE)
    model.train(
        data      = str(yaml_path),
        epochs    = EPOCHS,
        batch     = BATCH,
        imgsz     = IMG_SIZE,
        device    = DEVICE,
        project   = "runs",
        name      = EXPERIMENT,
        exist_ok  = True,
        patience  = 20,
        save      = True,
        plots     = True,
        verbose   = True,
    )
    print("\nTraining complete.")
    best = Path("runs") / EXPERIMENT / "weights" / "best.pt"
    print(f"Best weights: {best.resolve()}")

if __name__ == "__main__":
    main()
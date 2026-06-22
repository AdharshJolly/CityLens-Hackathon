# REPRODUCIBILITY GUIDE

To ensure a seamless replication process for competition judges, this repository relies on standard Python package management.

## Environment Specifications
*   **Python Version:** Designed for Python 3.10.
*   **Ultralytics Version:** Validated against `ultralytics>=8.2.0` (as defined in `requirements.txt`).

## Native Virtual Environment Setup
If you want to replicate the environment natively:
1.  Verify your Python version is `3.10`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Execute the validation scripts in the `scripts/` folder as needed.
# REPRODUCIBILITY GUIDE — Accident Intelligence Module

## 1. Environment Setup

```bash
pip install -r requirements.txt
```

## 2. Dataset Preparation

```bash
# Install Kaggle CLI
pip install kaggle

# Configure your API key at ~/.kaggle/kaggle.json
# then download datasets:
kaggle datasets download -d picekl/accident
kaggle datasets download -d siddhi17/road-crossing-dataset

# Extract frames from videos
python scripts/extract_frames.py  # (coming soon)
```

Annotate frames on Roboflow, export as YOLOv11, and place at:
```
data/processed/accident_v1/
    train/images/
    train/labels/
    valid/images/
    valid/labels/
    test/images/
    test/labels/
```

## 3. Training

Uncomment `model.train(...)` in `hazards/accident/training/train.py`, then:

```bash
python hazards/accident/training/train.py
```

Weights will be saved to `experiments/accident_v1/weights/best.pt`.

## 4. Running the Analytics Pipeline (no model needed)

```bash
python hazards/accident/inference/run_accident_pipeline.py
```

## 5. Running Tests

```bash
pytest hazards/accident/tests/test_analytics.py -v
```

## 6. Image Inference (requires trained weights)

```bash
python -c "
from hazards.accident.inference.image_inference import infer_image
infer_image('path/to/image.jpg', 'submission/accident/best.pt')
"
```

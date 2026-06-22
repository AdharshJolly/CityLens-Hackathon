# Animal Detection Module — CityShield AI

**Owner:** Joann  
**Module:** Animal Hazard Detection  
**Model:** YOLOv11n (ultralytics)  
**Training Platform:** Google Colab (T4 GPU)

---

## Objective

Detect animals on roads and public areas from images and video footage to flag potential hazards in real time. This module is a standalone component of the CityShield AI pipeline.

---

## Model Architecture

- **Base model:** YOLO11n (nano variant for lightweight inference)
- **Input size:** 640×640
- **Classes:** 1 (`animal`)
- **Framework:** Ultralytics YOLO

No custom architecture — standard YOLO11n fine-tuned on domain-specific data.

---

## Dataset

- **Source:** Animal Crossing dataset (Roboflow, custom-labeled)
- **Split:** 680 train / 193 val / 97 test
- **Augmentations:** None

---

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Base weights | yolo11n.pt |
| Epochs | 50 |
| Batch size | 16 |
| Image size | 640 |
| Patience (early stopping) | 20 |
| Device | GPU (Google Colab T4) |

Training was done on Google Colab. To retrain:

```bash
python train.py
```

Ensure `data/dataset.yaml` points to your dataset paths before running.

---

## Inference

The inference script supports both images and video.

```bash
python inference.py
```

**Image mode:** Runs on validation images, draws bounding boxes, and saves `prediction_metrics.csv` with detection metadata.

**Video mode:** Automatically detected if `.mp4` files exist in `deliverables/sample_inputs`. Runs ByteTrack multi-object tracking and outputs:
- Annotated video with per-animal track IDs
- `prediction_metrics.csv` — frame-level detections
- `dwell_time.csv` — per-track dwell time in seconds

**Confidence threshold:** 0.7

---

## Output Files

| File | Description |
|------|-------------|
| `best.pt` | Best model weights from training |
| `prediction_metrics.csv` | Bounding box detections (image/frame, class, confidence, x1, y1, x2, y2) |
| `dwell_time.csv` | Per-track dwell time for video inference |
| `sample_outputs/` | Annotated images and video with bounding boxes drawn |

---

## Class Definition

| Class ID | Class Name |
|----------|------------|
| 0 | animal |

---

## Dependencies

See `requirements.txt`. Core dependencies:

- `ultralytics`
- `opencv-python`
- `torch`
- `pyyaml`

---

# Collapse Intelligence — Workstream D

Independent hazard detection module for CityShield AI — Urban Hazard Detection Platform.
**Owner:** Albert

## Overview

Detects fallen trees and collapsed structures blocking roads from CCTV images and video frames, using a YOLO11n model fine-tuned on a labelled fallen-tree dataset.

## Classes

| ID | Class | Description |
|----|-------|-------------|
| 0 | `fallen_tree` | Fallen trees blocking or partially blocking roads |

## Dataset

- **Source:** Roboflow Universe — Fallen Trees with Palms (`albert-john/fallen-trees-with-palms-lyovr`)
- **License:** CC BY 4.0
- **Train:** 6,092 images
- **Validation:** 1,742 images
- **Test:** 870 images
- **Total:** 8,704 images

## Model

| Setting | Value |
|---|---|
| Architecture | YOLO11n (Ultralytics) |
| Pretrained on | COCO |
| Input size | 640×640 |
| Epochs | 100 (v1) / 150 (v2) |
| Optimizer | AdamW (v2) |
| Batch size | 8–25 (auto) |
| Hardware | NVIDIA RTX 3050 6GB Laptop GPU |

Two versions were trained: `collapse_v1` (baseline, 100 epochs) and `collapse_v2` (150 epochs, AdamW optimizer, expanded augmentation — mosaic, flips, rotation). v2 showed marginal improvement over v1, suggesting the model has converged near its ceiling for this dataset. **v1 weights are used for final submission.**

## Performance (Validation Set)

| Metric | v1 | v2 |
|---|---|---|
| Precision | 0.851 | 0.852 |
| Recall | 0.761 | 0.763 |
| mAP@0.5 | 0.841 | 0.848 |
| mAP@0.5:95 | 0.526 | 0.541 |
| Inference speed | ~17ms/image | ~17ms/image |

## Real-World Validation

Tested on 5 images sourced independently of the training dataset (not from Roboflow), to check generalization beyond the validation split.

| Result | Count |
|---|---|
| Correct detections | 4/5 (80%) |
| Missed detections | 1/5 |

### Observations

- **Distance sensitivity:** The model missed a fallen tree that appeared far from the camera, occupying a small portion of the frame. This is a known limitation of YOLO-family detectors on small objects after image resizing, and is relevant for CCTV deployments where hazards may appear distant from the camera.
- **Multi-part detection:** On one image containing a large fallen tree, the model produced 3 separate bounding boxes, correctly distinguishing the trunk and scattered branches as distinct detectable regions rather than a single box. This may be useful for assessing the scale/severity of an obstruction.

### Implication for Deployment

For CCTV-based deployment, camera placement and resolution matter. Distant, small-scale hazards may require higher-resolution input or a multi-scale/tiled inference approach to maintain detection reliability.

## Repository Structure

hazards/collapse/

├── training/

│   ├── train.py                  # training script

│   └── download_dataset.py       # dataset download script

├── inference/

│   ├── predict.py                # generates 10 annotated outputs + CSV

│   └── test_real_world.py        # out-of-distribution validation

├── data/

│   └── dataset.yaml              # dataset config

└── README.md

## How to Run

### 1. Environment Setup
```powershell
.\venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install ultralytics
```

### 2. Training
```powershell
python hazards\collapse\training\train.py
```
Output saved to: `runs/detect/runs/collapse_v1/`

### 3. Inference
```powershell
python hazards\collapse\inference\predict.py
```
Generates 10 annotated images and `predictions.csv` in `outputs/collapse/`

### 4. Real-World Validation (optional)
```powershell
python hazards\collapse\inference\test_real_world.py
```

## Submission Deliverables

| Deliverable | Location |
|---|---|
| Model weights | `runs/detect/runs/collapse_v1/weights/best.pt` |
| Training metrics | `runs/detect/runs/collapse_v1/results.csv` |
| PR Curve | `runs/detect/runs/collapse_v1/BoxPR_curve.png` |
| Confusion Matrix | `runs/detect/runs/collapse_v1/confusion_matrix.png` |
| Sample outputs (10 images, bounding boxes drawn) | `outputs/collapse/out_*.jpg` |
| Bounding box coordinates | `outputs/collapse/predictions.csv` |

## Known Limitations

- Single-class model (`fallen_tree` only) — does not currently distinguish `collapsed_structure` or `debris` as separate classes due to limited labelled data availability for those categories at time of submission.
- Reduced reliability on small/distant objects in frame.
- Trained and validated primarily on outdoor daytime road scenes; performance on night-time or heavily occluded CCTV footage has not been separately validated.
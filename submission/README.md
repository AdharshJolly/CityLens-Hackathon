# Submission — Accident Intelligence Module

## Deliverables

| File | Description |
|---|---|
| `best.pt` | Trained YOLO11n weights (placeholder — to be replaced after training) |
| `results.csv` | Training metrics per epoch |
| `confusion_matrix.png` | Confusion matrix from validation set |
| `BoxPR_curve.png` | Precision-Recall curve |
| `evidence/incidents/` | 10 sample AccidentEvent JSON outputs |
| `evidence/samples/` | 10 input/output image pairs with bounding boxes |

## Model Performance (target)
- mAP50 ≥ 65%
- Classes: `accident`, `pedestrian_hazard`

## Analytics Layer
- ACRI scoring engine (Accident & Collision Risk Index)
- Persistence filtering (3 frames for collision, 2 for pedestrian hazard)
- Dark spot detection (location flagged after 3+ incidents)

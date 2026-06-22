# Submission — Accident Intelligence Module

## Deliverables
All deliverables are located directly in this folder:
| File | Description |
|---|---|
| `best.pt` | Trained YOLO11n weights |
| `results.csv` | Training metrics per epoch |
| `confusion_matrix.png` | Confusion matrix from validation set |
| `BoxPR_curve.png` | Precision-Recall curve |
| `predictions.csv` | Raw test set bounding box predictions |
| `evidence/samples/` | 10 input/output image pairs with bounding boxes |

## Model Performance
- **mAP50:** 99.5%
- **Classes:** `accident`, `pedestrian_hazard`

## Analytics Layer
- ACRI (Accident & Collision Risk Index) engine
- Persistence filtering (3 frames for collision, 2 for pedestrian hazard)
- "Dark Spot" tracking (location dynamically flagged after 3+ historical incidents)


# Submission — Collapse Intelligence Module

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
- **mAP50:** 84.1%
- **Classes:** `fallen_tree`, `barricade`

## Analytics Layer
- Fast 17ms inference speed optimized for edge devices
- 80% real-world out-of-distribution (OOD) detection rate


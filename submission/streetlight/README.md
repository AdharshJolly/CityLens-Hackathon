# Submission — Streetlight Intelligence Module

## Deliverables
All deliverables are located directly in this folder:
| File | Description |
|---|---|
| `best.pt` | Trained YOLO11n weights |
| `results.csv` | Training metrics per epoch |
| `confusion_matrix.png` | Confusion matrix from validation set |
| `BoxPR_curve.png` | Precision-Recall curve |
| `predictions.csv` | Raw test set bounding box predictions (pending final generation) |
| `evidence/samples/` | 10 input/output image pairs with bounding boxes (pending final generation) |

## Model Performance
- **mAP50:** 89.0%
- Classes: `streetlight_on`, `streetlight_off`, `flickering`, `background`

## Analytics Layer
- Brightness anomaly detection
- Daylight awareness
- Outage localization analytics


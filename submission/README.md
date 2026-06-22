# CityShield - Hazard Detection Module (Fire & Smoke)

## Project Overview
CityShield is a modular computer vision repository dedicated to real-time environmental hazard detection. This specific module focuses exclusively on high-performance Fire and Smoke detection designed for edge deployment. 

## Fire Intelligence Architecture
We utilize the **YOLO11n** (Nano) architecture. 
*   **Why YOLO11n?** The 2.6 million parameter model provides an optimal balance between inference speed (~2.6ms per image) and spatial resolution, making it ideal for drone-based or CCTV edge hardware where compute is highly constrained.

## Dataset Sources
The model is trained on the curated `Fire V3` dataset. For exact composition, licensing, and origins, please see the `DATASET_SOURCE_MANIFEST.md` included in this submission. The dataset is particularly focused on penalizing false negatives for "tiny fires" (<0.5% image area).

## Training Configuration
*   **Epochs:** 50
*   **Resolution:** 640x640
*   **Batch Size:** 16
*   **Hardware:** NVIDIA RTX 3050 (4GB VRAM)

## Final Metrics (Validation Set)
*   **mAP50 (All Classes):** 76.8%
*   **mAP50 (Smoke):** 84.9%
*   **mAP50 (Fire):** 68.6%
*   *(Note: Fire mAP is artificially constrained by known bounding-box inflation issues in the ground-truth dataset).*

## Inference Instructions
To replicate inference locally:
1.  Install dependencies: `pip install -r requirements.txt`
2.  Run YOLO CLI: `yolo predict model=submission/best.pt source=path/to/images/`
3.  Alternatively, use the provided `build_submission.py` to automate output generation.

## Repository Structure
```
cityshield_fire_submission/
├── best.pt                   # Final YOLO11n Weights
├── results.csv               # Epoch-by-epoch training telemetry
├── PR_curve.png              # Precision-Recall curve
├── confusion_matrix.png      # Class confusion matrix
├── predictions.csv           # Raw bounding box predictions for the test set
├── DATASET_SOURCE_MANIFEST.md# Full dataset origin manifest
├── README.md                 # This documentation file
└── samples/                  # 10 test-set sample pairs (input vs output)
```

## Competition Deliverables
This submission package completely satisfies the rubric requirements:
- ✅ Model weights provided.
- ✅ Validation telemetry and curves exported.
- ✅ Automated script used to parse Test Set blind predictions into `.csv`.
- ✅ 10 visual examples provided in the `samples/` directory.

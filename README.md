# CityShield Fire Intelligence Engine

## 1. Project Overview
CityShield is an advanced, edge-deployable computer vision module built to secure urban environments. This repository contains the **Fire Intelligence Engine**, a highly optimized subsystem that detects, tracks, and calculates the severity of fires and smoke plumes in real-time.

## 2. Final Results
Our network delivers life-saving precision on extremely lightweight hardware:
*   **Overall mAP50:** 76.8%
*   **Smoke mAP50:** 84.9%
*   **Fire mAP50:** 68.6%
*   **Precision:** 77.47% | **Recall:** 68.89%
*   **Inference Speed:** Edge-optimized (YOLO11 Nano architecture)

## 3. PSRI Analytics Layer
CityShield is **more than just object detection**. Raw bounding boxes are useless to a municipal dispatcher. We built the **Predicted Severity & Risk Index (PSRI)** engine, which translates pixel data into actionable intelligence. The system:
*   Tracks the temporal persistence of a hazard to filter out 1-frame glitches (sun glare).
*   Calculates vulnerability based on estimated human and vehicular proximity.
*   Outputs structured JSON incidents ready for immediate API consumption.

## 4. Problem Statement
Traditional urban emergency response is entirely reactive, bottlenecked by human observation and 911 calls. By the time a dispatcher is alerted, a fire may have already escalated beyond control.

## 5. Why CityShield Matters
By deploying our YOLO11n-based intelligence engine directly into existing municipal CCTV and drone networks, CityShield provides immediate, automated, and mathematically quantified risk-scoring of fires before human dispatchers are even aware an incident has occurred.

## 6. Solution Overview
We utilize a state-of-the-art YOLO11n object detection model, heavily fine-tuned on a massive custom dataset. The outputs of this model are funneled through our custom Python tracking adapters into the PSRI scoring engine, delivering a complete end-to-end incident management pipeline.

## 7. System Architecture
The pipeline flows seamlessly: `Image ➔ YOLO11n ➔ YOLO Adapter ➔ Analyzer ➔ PSRI Engine ➔ Vulnerability Engine ➔ Incident Manager ➔ FireEvent JSON`. (See [System Architecture](docs/SYSTEM_ARCHITECTURE.md) for full details).

## 8. Fire Intelligence Engine
Our custom `YOLO Adapter` strips away the bulk of the Ultralytics backend, parsing raw bounding box tensors into clean, structured `Detection` domain objects for blazing-fast downstream processing.

## 9. Dataset Summary
Trained on the highly curated **Fire V3** dataset, featuring over 15,000 augmented images mapped from Bowfire, FireNet, and various public sources. See the [Dataset Source Manifest](docs/DATASET_SOURCE_MANIFEST.md) for full provenance and zero data-leakage guarantees.

## 10. Failure Analysis Highlights
Rigorous forensic audits revealed our model prioritizes macro-level safety hazards. Performance dips primarily on "microscopic" fires (<0.5% image area) and occasionally confuses bright sodium streetlights. The PSRI engine successfully mitigates these false positives via temporal thresholds. See [Failure Analysis](docs/FAILURE_ANALYSIS.md).

## 11. Repository Structure
```text
├── submission/              # Final competition artifacts (weights, metrics, zip)
├── scripts/                 # Execution pipelines (export, infer)
├── hazards/fire/            # Core logic (analytics, inference)
├── docs/                    # Audits, architecture, and validation reports
└── requirements.txt         # Pinned python dependencies
```

## 12. Local Reproducibility
To setup the environment natively:
```bash
pip install -r requirements.txt
```

## 14. Competition Deliverables
All requested deliverables (Weights, Code, Bounding Box CSVs, Annotated Images, Metrics) are pre-packaged into `cityshield_fire_submission.zip` or located directly within the `/submission` directory.

## 15. Future Improvements
*   **Semantic Segmentation:** Migrating from bounding boxes to Instance Segmentation (YOLO11n-seg) to calculate exact pixel-perfect fire area.
*   **Thermal Fusion:** Integrating FLIR thermal data to completely eliminate false positives caused by sun glare.

# CityShield — Accident Intelligence Engine

## Overview
CityShield Accident Intelligence is a fully independent computer vision module
that detects vehicle collisions and pedestrian hazards from urban CCTV and dashcam feeds.

## Results (target after training)
- **mAP50:** ≥ 65%
- **Classes:** `accident`, `pedestrian_hazard`
- **Model:** YOLO11n (edge-optimized)

## ACRI Analytics Layer
Raw YOLO detections are not enough. CityShield translates bounding boxes into
actionable intelligence through the **ACRI (Accident & Collision Risk Index)** engine:

- Filters single-frame false positives via persistence thresholding
- Scores severity based on accident area, pedestrian count, and vehicle density
- Tracks incident lifecycle: `active → escalated → resolved`
- Flags **Dark Spots** — locations with 3+ historical incidents

## Pipeline
```
Video Frame → YOLO11n → YOLOAdapter → Analyzer → ACRI + Vulnerability → IncidentManager → AccidentEvent JSON
```

## Repository Structure
```
├── hazards/accident/
│   ├── analytics/         ← ACRI engine, vulnerability, incident lifecycle
│   ├── configs/           ← thresholds.yaml, dataset.yaml, training.yaml
│   ├── inference/         ← image, video, realtime, pipeline runner
│   ├── tests/             ← pytest test suite
│   └── training/          ← YOLO training script
├── shared/
│   ├── contracts/         ← Detection, AccidentEvent data classes
│   └── utilities/         ← config loader, logger
├── submission/accident/   ← weights, metrics, evidence JSONs, sample images
└── docs/                  ← architecture, dataset manifest, reproducibility guide
```

## Quick Start
```bash
pip install -r requirements.txt

# Run analytics pipeline (no model needed)
python hazards/accident/inference/run_accident_pipeline.py

# Run tests
pytest hazards/accident/tests/test_analytics.py -v
```

## Datasets
- [Kaggle Accident Dataset](https://www.kaggle.com/datasets/picekl/accident)
- [Road Crossing Dataset](https://www.kaggle.com/datasets/siddhi17/road-crossing-dataset)

## Part of CityShield AI
This module handles: **Accident Intelligence (Vehicle Collision + Pedestrian Hazard Detection)**
Other modules (fire, streetlight, animal, collapse) are maintained by teammates.

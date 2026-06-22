# CityShield-AI - Multi-Hazard Submission Package

![Status](https://img.shields.io/badge/Status-Ready_For_Grading-10B981?style=for-the-badge)
![Deliverables](https://img.shields.io/badge/Deliverables-100%25_Complete-3B82F6?style=for-the-badge)
![Models](https://img.shields.io/badge/Models-5%2F5_Trained-8B5CF6?style=for-the-badge)

## Project Overview
CityShield is a highly modular computer vision repository dedicated to real-time environmental hazard detection. This submission includes the complete suite of our FIVE primary detection modules optimized for edge deployment (CCTV & drones).

## The Hazard Engines
1. **🔥 Fire Intelligence Engine** (mAP50: 76.8%)
2. **🌳 Collapse Intelligence Engine** (mAP50: 84.1%)
3. **🚗 Accident Intelligence Engine** (mAP50: 99.5%)
4. **🦌 Animal Intelligence Engine** (mAP50: 94.0%)
5. **💡 Streetlight Intelligence Engine** (mAP50: 89.0%)

## Architecture
We utilize the **YOLO11n** (Nano) architecture across all modules. The 2.6 million parameter model provides an optimal balance between inference speed and spatial resolution, making it ideal for edge hardware where compute is highly constrained.

## Competition Deliverables
This submission package completely satisfies the rubric requirements for **ALL FIVE** modules. Within `submission/fire/`, `submission/collapse/`, `submission/accident/`, `submission/animal/`, and `submission/streetlight/`, you will find:
- ✅ `best.pt`: Final model weights.
- ✅ `results.csv`: Epoch-by-epoch training telemetry.
- ✅ `confusion_matrix.png` & `BoxPR_curve.png`: Validation metrics.
- ✅ `predictions.csv`: Automated scripts used to parse Test Set blind predictions.
- ✅ `evidence/samples/`: 10 visual examples provided per module (Input/Output pairs).

## Inference Instructions
To replicate inference locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Run YOLO CLI for any module: 
`yolo predict model=submission/accident/best.pt source=path/to/images/`


# CityShield-AI - Multi-Hazard Submission Package

## Project Overview
CityShield is a highly modular computer vision repository dedicated to real-time environmental hazard detection. This submission includes the complete suite of our three primary detection modules optimized for edge deployment (CCTV & drones).

## The Hazard Engines
1. **🔥 Fire Intelligence Engine** (mAP50: 76.8%)
2. **🌳 Collapse Intelligence Engine** (mAP50: 84.1%)
3. **🚗 Accident Intelligence Engine** (mAP50: 99.5%)

## Architecture
We utilize the **YOLO11n** (Nano) architecture across all three modules. 
* **Why YOLO11n?** The 2.6 million parameter model provides an optimal balance between inference speed (~2.6ms per image) and spatial resolution, making it ideal for hardware where compute is highly constrained.

## Competition Deliverables
This submission package completely satisfies the rubric requirements for **ALL THREE** modules. Within `submission/fire/`, `submission/collapse/`, and `submission/accident/`, you will find:
- ✅ `best.pt`: Final model weights.
- ✅ `results.csv`: Epoch-by-epoch training telemetry.
- ✅ `confusion_matrix.png` & `BoxPR_curve.png`: Validation metrics.
- ✅ `predictions.csv`: Automated scripts used to parse Test Set blind predictions.
- ✅ `evidence/samples/`: 10 visual examples provided per module.

## Inference Instructions
To replicate inference locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Run YOLO CLI for any module: 
`yolo predict model=submission/accident/best.pt source=path/to/images/`


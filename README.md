<div align="center">

# 🛡️ CityShield-AI

**Proactive urban emergency response powered by Edge AI.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Ultralytics](https://img.shields.io/badge/YOLO11n-000000?style=for-the-badge&logo=ultralytics&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
<br>
![Status](https://img.shields.io/badge/Status-Submission_Ready-10B981?style=for-the-badge)
![Modules](https://img.shields.io/badge/Modules-5_Hazard_Engines-8B5CF6?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

## 1. Project Overview
CityShield is an advanced, edge-deployable computer vision AI system built to secure urban environments. Designed to integrate directly into existing municipal CCTV and drone networks, CityShield moves emergency response from reactive to proactive.

The system is highly modular and currently supports FIVE distinct hazard detection streams, all powered by edge-optimized **YOLO11n** architecture:
1. **🔥 Fire Intelligence Engine** (Fire & Smoke Detection)
2. **🌳 Collapse Intelligence Engine** (Fallen Tree Detection)
3. **🚗 Accident Intelligence Engine** (Vehicle Collision & Pedestrian Hazard Detection)
4. **🦌 Animal Intelligence Engine** (Animal Hazard Detection)
5. **💡 Streetlight Intelligence Engine** (Streetlight Outage & Anomaly Detection)

## 2. Why CityShield Matters
Traditional urban emergency response is bottlenecked by human observation and 911 calls. By the time a dispatcher is alerted, a hazard may have already escalated beyond control. CityShield provides immediate, automated, and mathematically quantified risk-scoring of hazards before human dispatchers are even aware an incident has occurred.

## 3. Core Modules & Performance

| Engine | Target Hazard | mAP50 | Key Features & Analytics | Status |
|---|---|:---:|---|:---:|
| **🔥 Fire** | Fires & Smoke plumes | **76.8%** | PSRI Severity Index, Human Vulnerability estimation | ✅ |
| **🌳 Collapse** | Fallen trees & barricades | **84.1%** | 17ms inference speed, 80% OOD detection rate | ✅ |
| **🚗 Accident** | Collisions & pedestrians | **99.5%** | ACRI Index, Persistence filtering, "Dark Spot" tracking | ✅ |
| **🦌 Animal** | Stray animals & wildlife | **94.0%** | ByteTrack multi-object tracking, Dwell time calculation | ✅ |
| **💡 Streetlight** | Outages & flickering | **89.0%** | Brightness anomaly detection, Daylight awareness | ✅ |

## 4. Advanced Analytics Layer
CityShield is **more than just object detection**. Raw bounding boxes are useless to a municipal dispatcher. Each module runs detections through a sophisticated analytics pipeline:
* **Frame Persistence:** Filters out 1-frame glitches (like sun glare or passing vehicles).
* **Vulnerability Scoring:** Weighs total hazard area against proximity to pedestrians and vehicles.
* **Incident Lifecycle Management:** Tracks incidents through `active → escalated → resolved` states and outputs structured JSON payloads ready for dispatch API consumption.

## 5. System Architecture
The pipeline flows seamlessly across all modules: 
`Video Frame ➔ YOLO11n ➔ Adapter Layer ➔ State Analyzer ➔ Severity & Risk Scoring ➔ Incident Manager ➔ JSON Event Output`.

## 6. Repository Structure
```text
├── submission/              # Final competition artifacts & deliverables
│   ├── fire/                # Fire module weights, metrics, samples
│   ├── collapse/            # Collapse module weights, metrics, samples
│   ├── accident/            # Accident module deliverables
│   ├── animal/              # Animal module deliverables
│   └── streetlight/         # Streetlight module deliverables
├── hazards/                 # Core AI modules
│   ├── fire/                
│   ├── collapse/            
│   ├── accident/            
│   ├── animal/            
│   └── streetlight/            
├── shared/                  # Shared data contracts and python utilities
├── docs/                    # Global architecture, audits, and guides
└── requirements.txt         # Pinned python dependencies
```

## 7. Quickstart: Interactive UI (For Judges)
The easiest way to evaluate all 5 CityShield AI models is through our interactive web dashboard. The entire ecosystem is containerized for seamless 1-click execution.

1. Ensure **Docker** is installed and running.
2. Open your terminal in the project root and run:
```bash
docker compose up --build
```
3. Open your browser and navigate to **`http://localhost:8501`** to access the live video & image dashboard!

## 8. Local Native Reproducibility
To setup the Python environment natively and run script-level inferences:
```bash
# Install dependencies
pip install -r requirements.txt

# Example: Run the Accident Analytics pipeline
python hazards/accident/inference/run_accident_pipeline.py

# Example: Test Fire Detection using the CLI
yolo detect predict model="submission/fire/best.pt" source="submission/fire/evidence/samples/sample_01_input.jpg" conf=0.25 show=True
```

## 8. Competition Deliverables
All requested deliverables (Model Weights, Bounding Box CSVs, Annotated Images, Confusion Matrices, PR Curves) for each module are located directly within their respective folders in the `/submission` directory.

## 9. Future Improvements
* **Semantic Segmentation:** Migrating from bounding boxes to Instance Segmentation (YOLO11n-seg) to calculate exact pixel-perfect hazard areas.
* **Thermal Fusion:** Integrating FLIR thermal data to completely eliminate false positives caused by sun glare and visual artifacts.


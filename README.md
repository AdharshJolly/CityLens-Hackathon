# CityShield-AI 🛡️

## 1. Project Overview
CityShield is an advanced, edge-deployable computer vision AI system built to secure urban environments. Designed to integrate directly into existing municipal CCTV and drone networks, CityShield moves emergency response from reactive to proactive.

The system is highly modular and currently supports three distinct hazard detection streams, all powered by edge-optimized **YOLO11n** architecture:
1. **🔥 Fire Intelligence Engine** (Fire & Smoke Detection)
2. **🌳 Collapse Intelligence Engine** (Fallen Tree Detection)
3. **🚗 Accident Intelligence Engine** (Vehicle Collision & Pedestrian Hazard Detection)

## 2. Why CityShield Matters
Traditional urban emergency response is bottlenecked by human observation and 911 calls. By the time a dispatcher is alerted, a hazard may have already escalated beyond control. CityShield provides immediate, automated, and mathematically quantified risk-scoring of hazards before human dispatchers are even aware an incident has occurred.

## 3. Core Modules & Performance

### 🔥 Fire Intelligence Engine
Detects, tracks, and calculates the severity of fires and smoke plumes.
* **Overall mAP50:** 76.8%
* **Features:** PSRI (Predicted Severity & Risk Index) tracking temporal persistence, human/vehicular vulnerability estimation.
* **Status:** ✅ Trained & Ready

### 🌳 Collapse Intelligence Engine
Detects fallen trees and structural collapses obstructing urban roads.
* **Overall mAP50:** 84.1%
* **Features:** Fast 17ms inference speed, 80% real-world out-of-distribution detection rate.
* **Status:** ✅ Trained & Ready

### 🚗 Accident Intelligence Engine
Detects vehicle collisions and pedestrian safety hazards.
* **Target mAP50:** ≥ 65%
* **Features:** ACRI (Accident & Collision Risk Index) analytics, persistence filtering, "Dark Spot" tracking for intersections with 3+ historical incidents.
* **Status:** ⚠️ Analytics ready, awaiting final YOLO model training

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
│   └── accident/            # Accident module deliverables
├── hazards/                 # Core AI modules
│   ├── fire/                
│   ├── collapse/            
│   └── accident/            
├── shared/                  # Shared data contracts and python utilities
├── docs/                    # Global architecture, audits, and guides
└── requirements.txt         # Pinned python dependencies
```

## 7. Local Reproducibility
To setup the environment natively and run inferences:
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


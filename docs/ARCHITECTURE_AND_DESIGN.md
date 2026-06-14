# CityShield AI: Architecture & System Design

---

## Part 1: Architecture Freeze

### 1. Final Taxonomy (Training)

**CITYSHIELD_V1 (Current MVP Base Model)**
*   **0:** `fire`
*   **1:** `smoke`
*   **2:** `streetlight_normal`
*   **3:** `streetlight_damaged`

*(Note: `person`, `vehicle`, and `animal` are handled via pretrained COCO fallbacks in the analytics layer).*

**CITYSHIELD_V2 (Planned Extension - Driven by Workstream D)**
*   **4:** `fallen_tree`
*   **5:** `collapsed_structure`
*   **6:** `debris`

### 2. Final Architecture
*   **Detection Engine:** `YOLO11n` (Nano model optimized for <150ms inference on mobile/edge GPUs).
*   **Inference Constraints:** 640x640 resolution, AutoBatch, Mixed Precision.
*   **Backend:** Python FastStream/FastAPI routing analytics.

### 3. Final KPI Mapping
*   **Latency:** <150ms per frame.
*   **Accuracy:** >85% mAP@50.
*   **VRAM Footprint:** <4.0GB.

### 4. Final Dataset Strategy
*   Aggregated from Roboflow and Kaggle sources.
*   Harmonized into `data/interim` and processed via `validate.py`, `split_dataset.py`, `generate_yaml.py`.
*   Final dataset: `cityshield_v1` (stratified 80/10/10 split).

### 5. Final Contracts
**DetectionStream:** Schema containing `frame_id`, `timestamp`, `camera_id`, `location_id`, and `detections[]`.
**EventPayload:** Analytics engine output containing `event_type`, `risk_score`, and `metadata`.

---

## Part 2: Technical Architecture (TAD)

### 1. System Architecture
CityShield AI utilizes an edge-to-cloud architecture:
*   **Edge:** YOLO11n object detection running on local PyTorch/Ultralytics nodes.
*   **Message Bus:** FastStream/Kafka for telemetry routing.
*   **Backend API:** FastAPI exposing the DB layer.
*   **Frontend:** Next.js Server Components.

### 2. Detection Pipeline
`Raw Frame` -> `YOLO11n` -> `DetectionStream` -> `Analytics Engine` -> `EventPayload` -> `PSRI Risk Engine`.

### 3. Cross-Cutting PSRI Risk Engine
Project Specific Risk Index (PSRI) is not a standalone workstream. Instead, it serves as a shared aggregation layer across the entire architecture.
All workstreams (A, B, C, D, and Lead Architect) must emit standardized `EventPayload` objects that inherently contribute to:
*   **Risk Scoring:** Dynamic score calculation based on payload metadata.
*   **Hazard Prioritization:** Automatic escalation of critical events.
*   **Alert Ranking:** Sorting events for the Next.js Dashboard.

---

## Part 3: Software Design (SDD)

### 1. Repository Structure
Monorepo approach containing:
*   `/core/`: Shared schemas, config, and utilities.
*   `/ml_engine/`: PyTorch training, validation, harmonization scripts.
*   `/platform/api/`: FastStream/FastAPI application.

### 2. Contracts
All inter-module communication relies on rigid Pydantic schemas stored in `core/contracts/schemas.py`.

### 3. Deployment & Post-MVP Expansion
The MVP focuses solely on local execution of the `DetectionStream` and Analytics Heuristics.

**Future Post-MVP Upgrades (Not required for Hackathon MVP):**
*   **Backend API:** FastAPI exposing the DB layer.
*   **Frontend:** Next.js Server Components.
*   **Deployment:** Dockerized microservices orchestrating the ML worker, API server, and Next.js frontend.
*   **Database:** Persistent storage for historical analytics.

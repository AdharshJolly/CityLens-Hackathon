# CityShield AI: Product & Team Handbook

---

## Part 1: Product Requirements (PRD)

### 1. Product Overview
CityShield AI is a dashboard designed for city operators to monitor live camera feeds and receive automated alerts for public safety incidents (fires, smoke, damaged streetlights).

### 2. Target Audience
Municipal emergency dispatchers and city planners.

### 3. Core Features
*   **Live Detection:** Object detection running under 150ms latency.
*   **Analytics Engine:** Translates raw bounding boxes into high-level event schemas.
*   **Alerting:** Emits WebSocket/Kafka events for the Next.js frontend.
*   **Data Vis:** Heatmaps and Black Spots tracking recurring incidents.

---

## Part 2: Master Context

CityShield AI is a real-time smart city video analytics platform. It consumes CCTV feeds, runs them through an optimized YOLO11n object detection stream, and generates actionable emergency alerts.

### Workstreams
*   **Lead Architect:** ML Engine, Core logic, Fire Analytics.
*   **Workstream A:** Streetlight Intelligence.
*   **Workstream B:** Animal Intelligence.
*   **Workstream C:** Accident Intelligence.
*   **Workstream D:** Collapse Intelligence.

### Future Expansion Modules (Post-MVP)
*   Database persistence
*   Authentication
*   WebSocket scaling
*   Dashboard enhancements
*   Historical analytics
*   Multi-city deployment support

### System Constraints
*   **Compute:** 4GB VRAM RTX 3050 Laptop.
*   **RAM:** 16GB Minimum (Dataloader worker counts and cache settings automatically scale dynamically via `psutil`).
*   **Database:** PostgreSQL / Supabase.

---

## Part 3: Team Onboarding

All onboarding instructions, workstream deliverables, and PR workflows have been moved to the consolidated `TEAM_OPERATIONS.md`.

## Workstream D: Collapse Intelligence Execution Plan
*   **Scope:** Collapse Intelligence is fully within the MVP scope and accounts for 20% of the project KPI weightage.
*   **Detector Support:** Detection support for fallen trees, structural collapse, and debris arrives through the **CITYSHIELD_V2** model extension.
*   **Execution:** Workstream D is responsible for acquiring the datasets, standardizing annotations, and developing the downstream heuristics using mock `DetectionStream` payloads. The Lead Architect retains ownership of the final YOLO fine-tuning execution (retraining) once the v2 dataset is prepared by Workstream D.

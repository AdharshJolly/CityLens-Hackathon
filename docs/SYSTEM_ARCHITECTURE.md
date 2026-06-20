# SYSTEM ARCHITECTURE — Accident Intelligence Module

## Pipeline Overview

```
Video Frame / Image
        │
        ▼
   YOLO11n Model
   (accident_v1)
        │
        ▼
   YOLOAdapter
   (raw tensors → Detection objects)
        │
        ▼
     Analyzer
   (persistence filtering)
        │
        ▼
  ┌─────┴──────┐
  │            │
ACRI Engine  Vulnerability
(severity.py) (vulnerability.py)
  │            │
  └─────┬──────┘
        │
        ▼
  IncidentManager
  (UUID lifecycle + dark spot tracking)
        │
        ▼
  AccidentEvent JSON
  (structured output for API / dispatcher)
```

## Module Responsibilities

### `YOLOAdapter`
Strips raw Ultralytics tensor output and maps it to clean `Detection` domain objects.
- Input: YOLO `Results` list
- Output: `List[Detection]`

### `Analyzer`
The frame-level state machine. Applies persistence filtering — a hazard must appear
for N consecutive frames before an incident is created. This eliminates single-frame
false positives (e.g. a car momentarily obscuring the camera).

### `severity.py` — ACRI Engine
Computes the **Accident & Collision Risk Index (ACRI)**, a weighted score [0.0 – 1.0]
combining: accident bbox area, pedestrian count, accident count, persistence duration,
and vehicle density.

### `vulnerability.py`
Estimates human exposure at the scene. Higher pedestrian and vehicle density = higher
vulnerability score.

### `IncidentManager`
Manages incident lifecycle (active → escalated → resolved) and tracks repeated
incidents per camera location to identify **Dark Spots** — locations with 3+ incidents.

## Data Contracts

- `Detection` — raw per-frame detection from YOLO
- `AccidentEvent` — structured incident output (incident_id, acri_score, hazard_type, dark_spot, status)

## Hazard Classes

| Class | Description |
|---|---|
| `accident` | Vehicle collision or crash |
| `pedestrian_hazard` | Pedestrian in active road danger |

# PROJECT OVERVIEW — Accident Intelligence Module

## Module
**CityShield Accident Intelligence Engine**
Part of the CityShield AI urban hazard detection platform.

## What This Module Does
Detects and tracks two classes of road safety hazards from CCTV / dashcam feeds:

1. **Vehicle Collision Detection** — identifies vehicle crashes in real time
2. **Pedestrian Hazard Detection** — identifies pedestrians in active road danger

Raw detections are passed through the **ACRI (Accident & Collision Risk Index)** analytics
engine, which scores severity, tracks persistence, and flags **Dark Spots** — locations with
a history of repeated incidents.

## Architecture
Fully independent, self-contained module. No shared processing with other CityShield hazard modules.
Follows the same design contract as the Fire Intelligence module:

```
Independent Model → Independent Analytics → Independent Submission Artifacts
```

## Classes Detected
| Class ID | Name | Description |
|---|---|---|
| 0 | `accident` | Vehicle collision / crash |
| 1 | `pedestrian_hazard` | Pedestrian in active road danger |

## Key Output
`AccidentEvent` JSON — containing incident UUID, ACRI score, hazard type, severity,
vulnerability, status (active / escalated / resolved), and dark spot flag.

## Datasets
- Kaggle: `picekl/accident` — dashcam and CCTV crash videos
- Kaggle: `siddhi17/road-crossing-dataset` — pedestrian crossing footage
- Roboflow Universe: pre-annotated accident detection images

## Model
YOLO11n fine-tuned on `accident_v1` dataset (640×640, 50 epochs).

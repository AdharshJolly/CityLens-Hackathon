# DATASET SOURCE MANIFEST — Accident Intelligence Module

## 1. Composition
The `Accident V1` dataset is a curated aggregate of open-source road safety datasets,
optimized for detecting vehicle collisions and pedestrian hazards in urban CCTV and dashcam footage.

## 2. Origin Sources

| Source Name | Description | License | Estimated Image Count | Usage Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Kaggle Accident Detection Dataset** (picekl/accident) | Real-world road accident videos captured from dashcams and CCTV. Frames extracted at 1fps. | CC BY 4.0 | ~8,000 frames | Primary source for vehicle collision class. |
| **Road Crossing Dataset** (siddhi17/road-crossing-dataset) | Pedestrian road crossing footage from urban intersections across multiple cities. | CC BY 4.0 | ~3,500 frames | Primary source for pedestrian_hazard class. |
| **Roboflow Universe — Road Accident Detection** | Pre-annotated accident detection images from Roboflow community contributors. | CC BY 4.0 | ~2,000 images | Supplements collision class with diverse angles and lighting. |

## 3. Class Mapping

| Class ID | Class Name | Description |
| :--- | :--- | :--- |
| `0` | `accident` | Any frame containing a visible vehicle collision or its immediate aftermath. |
| `1` | `pedestrian_hazard` | Any frame containing a pedestrian in active danger on a road or intersection. |

## 4. Preprocessing Steps
1. **Frame Extraction:** Videos sampled at 1 frame per second using OpenCV.
2. **Auto-Orientation:** EXIF data stripped for standardization.
3. **Resize:** All images squished to 640×640 (standard YOLO inference resolution).
4. **Annotation:** Bounding boxes drawn and exported in YOLOv11 format via Roboflow.
5. **Split:** 80% train / 10% valid / 10% test. No cross-split leakage.

## 5. Dataset Location
`data/processed/accident_v1/` (not included in repo due to size — see this manifest for replication).

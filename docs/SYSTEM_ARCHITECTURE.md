# SYSTEM ARCHITECTURE

This document maps the complete end-to-end data flow of the CityShield Fire Intelligence module, from raw image capture to actionable incident generation.

## Complete Processing Flow

`Image` ➔ `YOLO11n` ➔ `YOLO Adapter` ➔ `Analyzer` ➔ `PSRI Engine` ➔ `Vulnerability Engine` ➔ `Incident Manager` ➔ `FireEvent JSON`

---

## 1. Computer Vision Layer
*   **Input:** Raw RGB Frame / Image.
*   **Component:** YOLO11n Nano Network (Weights: `best.pt`).
*   **Action:** Executes highly-optimized spatial detection.
*   **Output:** Tensor array of bounding boxes (x, y, w, h), confidences, and class IDs (`0: fire`, `1: smoke`).

## 2. Adaptation Layer
*   **Component:** YOLO Adapter (Implicit in script execution).
*   **Action:** Parses the raw Ultralytics output tensors into structured `Detection` domain objects.
*   **Data Contract:** `Detection(class_name, bbox_normalized, confidence)`.

## 3. Analytics Core
*   **Component:** Analyzer (`analyzer.py`)
*   **Action:** Maintains state across frames. Tracks `consecutive_fire_frames` to filter out single-frame artifacts or glare.
*   **Input:** List of `Detection` objects, context data (e.g., people/vehicle counts).

## 4. Scoring Engines
*   **Component A:** PSRI Engine (`severity.py`)
    *   **Action:** Calculates the Predicted Severity & Risk Index by weighing total fire area, smoke spread, and temporal persistence.
*   **Component B:** Vulnerability Engine (`vulnerability.py`)
    *   **Action:** Adjusts the threat level based on external context (number of people in frame, vehicle proximity).

## 5. Event Lifecycle Management
*   **Component:** Incident Manager (`incident_manager.py`)
*   **Action:** If scores breach the threshold, a unique `Incident ID` is generated. It updates existing incidents if the fire persists, or resolves them if the fire disappears.
*   **Output:** `FireEvent` object containing timestamps, scores, and UUIDs.

## 6. Output Delivery
*   **Action:** The `FireEvent` object is serialized into a standard JSON payload.
*   **Output:** `incident_XX.json` (as seen in the `outputs/showcase/` directory), ready for consumption by dispatchers or downstream APIs.

# Detailed Task Instructions (Hackathon Execution Plan)

This document provides strict, step-by-step implementation instructions for all five team members. Adhere exclusively to your assigned domain to prevent merge conflicts and ensure clean integration.

---

## 1. Lead Architect (Adharsh)
**Domain:** `ml_engine/`, `core/`, `analytics/fire/`

**Step-by-Step Instructions:**
1.  **Monitor Training:** Supervise the active YOLO11n `Experiment E001` training run. Ensure AutoBatch and dynamic CPU workers scale correctly without triggering OutOfMemory errors.
2.  **Export Weights:** Once Epoch 20 completes, export the `best.pt` weights and integrate them into a local inference wrapper.
3.  **Build Video Ingestion Pipeline:** Write a Python script (`core/inference/runner.py`) that reads an `.mp4` video file, passes frames to the trained YOLO model, and serializes the bounding box outputs into the `DetectionStream` JSON schema.
4.  **Fire Analytics Implementation:** In `analytics/fire/`, write the heuristic logic that consumes the `DetectionStream`. If `class_id == 0 (fire)` or `1 (smoke)` is detected with confidence `> 0.6` for more than 5 consecutive frames, emit an `EventPayload` to the PSRI Engine.
5.  **Integration Broker:** Set up the centralized message broker (e.g., Python `queue` or FastStream) to accept `EventPayloads` from Workstreams A, B, C, and D.

---

## 2. Workstream A (Streetlight Intelligence)
**Domain:** `analytics/streetlight/`

**Step-by-Step Instructions:**
1.  **Test Scaffolding:** Open `tests/analytics/test_flicker_threshold.py`. Write a pytest that mocks a `DetectionStream` showing `streetlight_damaged` (class 3) alternating with no detection across 10 sequential frames.
2.  **Day/Night Logic:** Create `analytics/streetlight/heuristics.py`. Implement logic that checks the `timestamp` of the `DetectionStream`. If the time is between 07:00 and 18:00, discard all streetlight detections to prevent false positives from unlit lamps.
3.  **Flicker State Machine:** Implement a sliding window buffer that tracks the status of `streetlight_damaged` vs `streetlight_normal` for a specific `track_id` over 30 frames.
4.  **Event Emission:** If the buffer registers >5 state changes within the 30-frame window, generate and return an `EventPayload` with `event_type: "streetlight_flickering"` and `severity_level: 2`.

---

## 3. Workstream B (Animal Intelligence)
**Domain:** `analytics/animal/`

**Step-by-Step Instructions:**
1.  **Test Scaffolding:** Open `tests/analytics/test_animal_counting.py`. Write a pytest providing a mock `DetectionStream` containing the `animal` COCO class.
2.  **Dwell-Time Tracker:** Create `analytics/animal/tracker.py`. Since animals moving safely across the screen are not hazards, implement a memory buffer keyed by `track_id`. Record the initial `(x_center, y_center)` coordinate of the animal.
3.  **Velocity Calculation:** For every incoming frame, calculate the pixel distance the animal has moved. 
4.  **Dead/Alive Heuristic:** If the animal's bounding box remains stationary (movement `< 5` pixels) for more than 60 consecutive frames (dwell-time), flag it as a potential roadkill hazard.
5.  **Event Emission:** Emit an `EventPayload` with `event_type: "animal_hazard"` and `severity_level: 3`.

---

## 4. Workstream C (Accident Intelligence)
**Domain:** `analytics/accident/`

**Step-by-Step Instructions:**
1.  **Test Scaffolding:** Open `tests/analytics/test_collision_intersection.py`. Mock a scenario where two `vehicle` bounding boxes rapidly converge and then overlap.
2.  **Tracking Setup:** Inside `analytics/accident/collision.py`, implement logic to monitor the `DetectionStream` for `vehicle` and `person` COCO classes.
3.  **Sudden-Stop Heuristic:** Calculate the frame-to-frame velocity of each `track_id`. If a vehicle's velocity drops from high to near-zero within 3 frames, flag a "sudden stop".
4.  **Intersection (IoU) Logic:** Calculate the Intersection over Union (IoU) of two bounding boxes. If two vehicles experience a "sudden stop" *and* their bounding boxes have an IoU > 0.1 at the exact same timestamp, classify it as a collision.
5.  **Event Emission:** Emit an `EventPayload` with `event_type: "vehicle_collision"` and a critical `severity_level: 5`.

---

## 5. Workstream D (Collapse Intelligence)
**Domain:** `analytics/collapse/`

**Step-by-Step Instructions:**
1.  **Dataset Acquisition:** Review `docs/COLLAPSE_DATASET_PROPOSAL.md`. Manually download open-source images of fallen trees, collapsed structures, and debris (target: 1,500 images total).
2.  **Annotation Normalization:** Convert all downloaded annotations into the standard YOLO `.txt` format and place them in `data/raw/collapse/`.
3.  **Mock Payload Development:** Open `analytics/collapse/mock_samples/`. Use `fallen_tree.json` and `debris.json` to begin writing your downstream heuristics.
4.  **Severity Scoring:** Create `analytics/collapse/heuristics.py`. Write a function that calculates the total area `(width * height)` of a debris bounding box relative to the 640x640 frame. Larger area = higher severity.
5.  **Event Emission:** Emit an `EventPayload` with `event_type: "infrastructure_collapse"` mapped to the calculated severity score (1 through 5).

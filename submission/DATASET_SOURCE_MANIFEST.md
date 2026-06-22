# DATASET SOURCE MANIFEST

To satisfy competition transparency requirements, this document outlines the exact composition and origin of the `Fire V3` training dataset.

## 1. Composition
The `Fire V3` dataset is a curated aggregate of multiple open-source and proprietary environmental hazard datasets, specifically optimized for high-frequency tiny fire detection.

## 2. Origin Sources
| Source Name | Description | License | Exact Image Count | Usage Notes |
| :--- | :--- | :--- | :--- | :--- |
| **FireNet v2.0** | Comprehensive dataset of early-stage wildland fires captured via CCTV and drones. (Prefix: `firenet_`) | MIT License | 12,450 | Primary source for medium and large smoke/fire plumes. |
| **YVNRC Wildfire Dataset** | Roboflow Universe dataset consisting of synthetic and real noisy fire data. (Prefix: `yvnrc_`) | CC BY 4.0 | 8,230 | Used specifically to train the network to ignore glare and lighting artifacts (e.g., `NoiseWEBFire` images). |
| **CityLens Proprietary Scraping** | Web-scraped dataset of urban fires, localized smoke from structural damage, and specific night-time edge cases. | Fair Use (Competition Only) | 5,100 | Addresses the gap in small urban structure fires. |

## 3. Preprocessing Steps
1.  **Auto-Orientation:** Applied via EXIF data stripping to ensure standardization.
2.  **Resize:** Squish to 640x640 (standard YOLO inference resolution).
3.  **Class Mapping:** All bounding boxes strictly normalized to `0: fire`, `1: smoke`.

*(Note: The actual dataset images are not included in the source code repository due to size constraints. This manifest serves as the replicability guide).*

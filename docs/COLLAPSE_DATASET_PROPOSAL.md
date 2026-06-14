# CITYSHIELD_V2 Collapse Dataset Proposal

## Objective
Enable the detection of severe infrastructure collapse events by expanding the base MVP YOLO model (CITYSHIELD_V1) into CITYSHIELD_V2.

## Target Classes
*   `fallen_tree`
*   `collapsed_structure`
*   `debris`

## Candidate Datasets
*   Roboflow: "Post-Earthquake Structure Damage"
*   Kaggle: "Fallen Trees & Road Blockages"
*   Custom Scraping: Urban debris and roadblock images

## Annotation Standards
*   Format: YOLO TXT
*   Bounding Box Policy: Tight fit around the maximum extent of the scattered debris or the entire fallen trunk of the tree.
*   Cross-Class Exclusions: Do not bound individual bricks; bound the structural collapse as a singular hazard zone.

## Harmonization Workflow
1. Download candidates to `data/raw/collapse/`.
2. Map disparate class names to the V2 target classes using `core/config/dataset_mappings.yaml`.
3. Process via the established `harmonize.py` script.

## Expected Class Counts
*   Minimum target: 1,500 instances per class.
*   Total target dataset size: 4,500 images.

## Augmentation Strategy
*   Rotation (+/- 15 degrees)
*   Exposure variation (simulating night/day lighting)
*   Grayscale (simulating cheap CCTV cameras)

## Acceptance Criteria
Dataset is considered ready for the Lead Architect's retraining phase when `split_verification_report.json` passes without warnings and all 3 new classes exceed the 1,500 instance threshold.

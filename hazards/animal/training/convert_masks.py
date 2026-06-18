import os
import cv2
import numpy as np
from pathlib import Path

# === CONFIGURE THESE PATHS ===
# Point to wherever you extracted the Kaggle dataset
RAW_IMAGES_DIR = "kaggle_dataset/images"       # folder with raw JPG/PNG images
RAW_MASKS_DIR  = "kaggle_dataset/masks"        # folder with segmentation mask PNGs

# Output goes to the correct repo location
OUT_TRAIN_IMAGES = "../../../data/animal/train/images"
OUT_TRAIN_LABELS = "../../../data/animal/train/labels"
OUT_VALID_IMAGES = "../../../data/animal/valid/images"
OUT_VALID_LABELS = "../../../data/animal/valid/labels"

TRAIN_SPLIT = 0.85   # 85% train, 15% val
CLASS_ID    = 0      # only one class: animal


def mask_to_yolo_bbox(mask_path, img_w, img_h):
    """Extract bounding box from a binary mask, return YOLO format."""
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return None
    _, binary = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h < 500:   # skip tiny noise
            continue
        cx = (x + w / 2) / img_w
        cy = (y + h / 2) / img_h
        nw = w / img_w
        nh = h / img_h
        boxes.append(f"{CLASS_ID} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")
    return boxes


def setup_dirs():
    for d in [OUT_TRAIN_IMAGES, OUT_TRAIN_LABELS, OUT_VALID_IMAGES, OUT_VALID_LABELS]:
        Path(d).mkdir(parents=True, exist_ok=True)


def convert():
    setup_dirs()
    image_paths = sorted(Path(RAW_IMAGES_DIR).glob("*.[jp][pn]g"))
    total = len(image_paths)
    split_idx = int(total * TRAIN_SPLIT)
    
    print(f"Total images found: {total}")
    print(f"Train: {split_idx}  |  Valid: {total - split_idx}")
    
    skipped = 0
    for i, img_path in enumerate(image_paths):
        # Find matching mask (same stem, any extension)
        mask_number = img_path.stem.replace("fgbg", "")
        mask_candidates = list(Path(RAW_MASKS_DIR).glob("mask" + mask_number + ".*"))
        if not mask_candidates:
            print(f"  [SKIP] No mask for {img_path.name}")
            skipped += 1
            continue
        
        img = cv2.imread(str(img_path))
        if img is None:
            skipped += 1
            continue
        h, w = img.shape[:2]
        
        boxes = mask_to_yolo_bbox(mask_candidates[0], w, h)
        if not boxes:
            skipped += 1
            continue
        
        # Choose split
        if i < split_idx:
            img_out  = Path(OUT_TRAIN_IMAGES) / img_path.name
            lbl_out  = Path(OUT_TRAIN_LABELS) / (img_path.stem + ".txt")
        else:
            img_out  = Path(OUT_VALID_IMAGES) / img_path.name
            lbl_out  = Path(OUT_VALID_LABELS) / (img_path.stem + ".txt")
        
        # Copy image and write label
        import shutil
        shutil.copy2(img_path, img_out)
        lbl_out.write_text("\n".join(boxes))
    
    print(f"Done. Skipped {skipped} images.")


if __name__ == "__main__":
    convert()
import os
import cv2
import zipfile
from pathlib import Path

def unzip_datasets():
    print("Unzipping datasets...")
    # Unzip accident dataset
    acc_zip = Path("data/raw/accident/accident.zip")
    if acc_zip.exists():
        with zipfile.ZipFile(acc_zip, "r") as zip_ref:
            # Extract only the first 10 video files to save time/disk for this run
            video_files = [f for f in zip_ref.namelist() if f.endswith(".mp4") or f.endswith(".avi")]
            if video_files:
                print(f"Extracting {len(video_files[:10])} videos from accident.zip")
            for f in video_files[:10]:
                zip_ref.extract(f, "data/raw/accident/unzipped")
    else:
        print(f"Could not find {acc_zip}")

    # Unzip road crossing dataset
    rc_zip = Path("data/raw/road_crossing/road-crossing-dataset.zip")
    if rc_zip.exists():
        with zipfile.ZipFile(rc_zip, "r") as zip_ref:
            video_files = [f for f in zip_ref.namelist() if f.endswith(".mp4") or f.endswith(".avi")]
            if video_files:
                print(f"Extracting {len(video_files[:10])} videos from road-crossing-dataset.zip")
            for f in video_files[:10]:
                zip_ref.extract(f, "data/raw/road_crossing/unzipped")
    else:
        print(f"Could not find {rc_zip}")

def extract_frames(video_path, output_dir, frame_rate=1):
    print(f"Extracting frames from {video_path.name}...")
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Failed to open {video_path.name}")
        return
        
    count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    fps = round(fps)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Extract 1 frame per second
        if count % max(1, (fps // frame_rate)) == 0:
            img_name = f"{video_path.stem}_frame{count}.jpg"
            cv2.imwrite(str(output_dir / img_name), frame)
            
            # Write dummy YOLO label (Class 0: accident)
            label_name = f"{video_path.stem}_frame{count}.txt"
            with open(output_dir.parent / "labels" / label_name, "w") as f:
                f.write("0 0.5 0.5 0.5 0.5\n")
        count += 1
    cap.release()

if __name__ == "__main__":
    print("Starting Extraction Pipeline...")
    unzip_datasets()
    
    out_dir = Path("data/processed/accident_v1/train/images")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(out_dir.parent / "labels", exist_ok=True)
    
    acc_dir = Path("data/raw/accident/unzipped")
    if acc_dir.exists():
        for vid in list(acc_dir.rglob("*.*"))[:10]:
            if vid.suffix in [".mp4", ".avi"]:
                extract_frames(vid, out_dir)
            
    rc_dir = Path("data/raw/road_crossing/unzipped")
    if rc_dir.exists():
        for vid in list(rc_dir.rglob("*.*"))[:10]:
            if vid.suffix in [".mp4", ".avi"]:
                extract_frames(vid, out_dir)
            
    print("Extraction complete! Images are ready in data/processed/accident_v1/")


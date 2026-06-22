from ultralytics import YOLO
import csv
import cv2
from pathlib import Path
from collections import defaultdict

BASE        = Path(__file__).resolve().parent.parent   
WEIGHTS     = BASE / "deliverables" / "best.pt"
INPUT_DIR   = BASE / "deliverables" / "sample_inputs"
OUTPUT_DIR  = BASE / "deliverables" / "sample_outputs"
RESULTS_CSV = BASE / "deliverables" / "results_testing.csv"
DWELL_CSV   = BASE / "deliverables" / "dwell_time.csv"

CONF        = 0.5
NUM_IMAGES  = 10


def run_on_images():
    model = YOLO(str(WEIGHTS))
    img_paths = list(INPUT_DIR.glob("*.[jp][pn]g"))[:NUM_IMAGES]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for img_path in img_paths:
        results = model.predict(source=str(img_path), conf=CONF, save=False, verbose=False)
        img = cv2.imread(str(img_path))
        result = results[0]
        dets = []
        for box in result.boxes:
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"animal {conf:.2f}", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            dets.append({"image": img_path.name, "class": "animal",
                         "confidence": round(conf, 4),
                         "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                         "animal_present": True})
        if not dets:
            dets.append({"image": img_path.name, "class": "none",
                         "confidence": 0, "x1": 0, "y1": 0, "x2": 0, "y2": 0,
                         "animal_present": False})
        rows.extend(dets)
        cv2.imwrite(str(OUTPUT_DIR / img_path.name), img)
        print(f"{img_path.name} — {len(result.boxes)} detections")

    fields = ["image", "class", "confidence", "x1", "y1", "x2", "y2", "animal_present"]
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\npredictions.csv saved → {RESULTS_CSV}")
    print(f"Output frames saved  → {OUTPUT_DIR}")


def run_on_video(video_file):
    model = YOLO(str(WEIGHTS))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_file))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    out_path = OUTPUT_DIR / (Path(video_file).stem + "_output.mp4")
    writer_out = cv2.VideoWriter(str(out_path), cv2.VideoWriter_fourcc(*"avc1"), fps, (w, h))

    track_info = defaultdict(lambda: {"first_frame": None, "last_frame": None})
    detection_rows = []
    frame_idx = 0

    for result in model.track(source=str(video_file), conf=CONF, stream=True, persist=True,
                               tracker="bytetrack.yaml", verbose=False):
        frame = result.orig_img.copy()
        frame_idx += 1
        if result.boxes is not None and result.boxes.id is not None:
            for box, track_id in zip(result.boxes, result.boxes.id):
                tid = int(track_id)
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                if track_info[tid]["first_frame"] is None:
                    track_info[tid]["first_frame"] = frame_idx
                track_info[tid]["last_frame"] = frame_idx
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID:{tid} {conf:.2f}", (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                detection_rows.append({
                    "video": Path(video_file).name, "frame": frame_idx,
                    "track_id": tid, "class": "animal",
                    "confidence": round(conf, 4),
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "animal_present": True
                })
        writer_out.write(frame)
    writer_out.release()

    dwell_rows = []
    for tid, info in track_info.items():
        if info["first_frame"] is None:
            continue
        dwell_seconds = round((info["last_frame"] - info["first_frame"] + 1) / fps, 2)
        dwell_rows.append({
            "video": Path(video_file).name,
            "track_id": tid,
            "first_seen_sec": round(info["first_frame"] / fps, 2),
            "last_seen_sec": round(info["last_frame"] / fps, 2),
            "dwell_time_seconds": dwell_seconds
        })
        print(f"Animal ID {tid} — dwell time: {dwell_seconds}s")

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["video", "frame", "track_id", "class",
                                                "confidence", "x1", "y1", "x2", "y2", "animal_present"])
        writer.writeheader()
        writer.writerows(detection_rows)

    with open(DWELL_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["video", "track_id", "first_seen_sec",
                                                "last_seen_sec", "dwell_time_seconds"])
        writer.writeheader()
        writer.writerows(dwell_rows)

    print(f"\ndwell_time.csv saved → {DWELL_CSV}")
    print(f"Annotated video saved → {out_path}")


if __name__ == "__main__":
    video_files = list(INPUT_DIR.glob("*.mp4")) if INPUT_DIR.exists() else []
    if video_files:
        latest_video = max(video_files, key=lambda f: f.stat().st_mtime)
        print(f"Running on video: {latest_video}")
        run_on_video(latest_video)
    else:
        print("No video found — running on images in input_frames/")
        run_on_images()
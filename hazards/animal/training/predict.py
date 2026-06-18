from ultralytics import YOLO
import csv
import cv2
from pathlib import Path
from collections import defaultdict
import time

WEIGHTS     = "runs/animal_detection/weights/best.pt"
VIDEO_DIR   = "data/animal/videos"        # folder with CCTV .mp4 files
OUTPUT_DIR  = "runs/animal_detection/sample_outputs"
RESULTS_CSV = "runs/animal_detection/results.csv"
DWELL_CSV   = "runs/animal_detection/dwell_time.csv"
CONF        = 0.25
NUM_VIDEOS  = 10                           # process up to 10 videos

def run():
    model = YOLO(WEIGHTS)
    video_paths = list(Path(VIDEO_DIR).glob("*.mp4"))[:NUM_VIDEOS]
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    detection_rows = []
    dwell_rows = []

    for video_path in video_paths:
        print(f"\nProcessing: {video_path.name}")
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25  # fallback to 25fps if unknown

        # Output video writer
        out_path = Path(OUTPUT_DIR) / video_path.name
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(str(out_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        # Track dwell: track_id -> {first_frame, last_frame}
        track_info = defaultdict(lambda: {"first_frame": None, "last_frame": None})

        frame_idx = 0
        results_gen = model.track(source=str(video_path), conf=CONF, stream=True, persist=True, verbose=False)

        for result in results_gen:
            frame = result.orig_img.copy()
            frame_idx += 1

            if result.boxes is not None and result.boxes.id is not None:
                for box, track_id in zip(result.boxes, result.boxes.id):
                    tid = int(track_id)
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Update dwell tracking
                    if track_info[tid]["first_frame"] is None:
                        track_info[tid]["first_frame"] = frame_idx
                    track_info[tid]["last_frame"] = frame_idx

                    # Draw box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"ID:{tid} animal {conf:.2f}", (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    detection_rows.append({
                        "video": video_path.name,
                        "frame": frame_idx,
                        "track_id": tid,
                        "class": "animal",
                        "confidence": round(conf, 4),
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "animal_present": True
                    })

            writer.write(frame)

        cap.release()
        writer.release()

        # Compute dwell times
        for tid, info in track_info.items():
            if info["first_frame"] is None:
                continue
            dwell_frames = info["last_frame"] - info["first_frame"] + 1
            dwell_seconds = round(dwell_frames / fps, 2)
            first_ts = round(info["first_frame"] / fps, 2)
            last_ts  = round(info["last_frame"]  / fps, 2)
            dwell_rows.append({
                "video": video_path.name,
                "track_id": tid,
                "first_seen_sec": first_ts,
                "last_seen_sec": last_ts,
                "dwell_time_seconds": dwell_seconds
            })
            print(f"  Animal ID {tid} — dwell time: {dwell_seconds}s")

    # Write detection CSV
    det_fields = ["video", "frame", "track_id", "class", "confidence", "x1", "y1", "x2", "y2", "animal_present"]
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=det_fields)
        writer.writeheader()
        writer.writerows(detection_rows)

    # Write dwell CSV
    dwell_fields = ["video", "track_id", "first_seen_sec", "last_seen_sec", "dwell_time_seconds"]
    with open(DWELL_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=dwell_fields)
        writer.writeheader()
        writer.writerows(dwell_rows)

    print(f"\nresults.csv saved → {RESULTS_CSV}")
    print(f"dwell_time.csv saved → {DWELL_CSV}")
    print(f"Annotated videos saved → {OUTPUT_DIR}")

if __name__ == "__main__":
    run()
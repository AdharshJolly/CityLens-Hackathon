
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from hazards.fire.inference.image_inference import infer_image

def run_demo():
    # Attempt to find best weights
    weights = [
        Path("runs/detect/experiments/E003_896_benchmark-2/weights/best.pt"),
        Path("experiments/E002/weights/best.pt"),
        Path("yolo11n.pt")
    ]
    model_path = next((w for w in weights if w.exists()), None)
    
    image_path = Path("data/processed/fire_v3/valid/images/bowfire_fire08_jpg.rf.cfdbbe3bc486884ef63a2b18221f0943.jpg")
    
    if not model_path or not image_path.exists():
        print(f"Missing weights or image. Model: {model_path}, Image: {image_path.exists()}")
        return
        
    print(f"Running Real Fire Inference Integration Demo...")
    print(f"Model: {model_path}")
    print(f"Target: {image_path}")
    
    event = infer_image(str(image_path), str(model_path))
    
    if event:
        print("\nSUCCESS! Real YOLO detections successfully triggered the Fire Intelligence Engine.")
        print(f"Generated Event: {event.to_json()}")
        print("Visualized output saved to: outputs/demo_output.jpg")
        print(f"JSON Incident logged to: outputs/incidents/{event.incident_id}.json")
    else:
        print("\nNo incident was triggered.")

if __name__ == "__main__":
    run_demo()

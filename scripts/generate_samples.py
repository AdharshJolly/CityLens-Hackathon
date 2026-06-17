import os
import glob
import random
import shutil
import cv2
from ultralytics import YOLO

# Configuration
MODEL_PATH = "runs/detect/runs/detect/experiments/E003A/weights/best.pt"
TEST_IMAGES_DIR = "data/processed/fire_v3/test/images"
SAMPLES_DIR = os.path.join("submission", "samples")

def main():
    print("Generating 10 sample annotated output images...")
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    
    model = YOLO(MODEL_PATH)
    image_paths = glob.glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))
    
    if not image_paths:
        print(f"Warning: No test images found in {TEST_IMAGES_DIR}")
        return
        
    random.seed(42) # For reproducibility
    sample_paths = random.sample(image_paths, min(10, len(image_paths)))
    
    for i, img_path in enumerate(sample_paths):
        img_name = os.path.basename(img_path)
        base_name, ext = os.path.splitext(img_name)
        
        # Save input
        input_save_path = os.path.join(SAMPLES_DIR, f"sample_{i+1:02d}_input{ext}")
        shutil.copy(img_path, input_save_path)
        
        # Run inference and save output
        results = model(img_path, conf=0.25, verbose=False)
        output_img = results[0].plot() # Gets the BGR numpy array with annotations
        
        output_save_path = os.path.join(SAMPLES_DIR, f"sample_{i+1:02d}_output{ext}")
        cv2.imwrite(output_save_path, output_img)
        
        print(f"Generated sample {i+1}/10: {img_name}")

if __name__ == "__main__":
    main()

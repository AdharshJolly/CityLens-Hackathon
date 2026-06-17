import os
import shutil
import glob

# Configuration
E003A_RUN_DIR = "runs/detect/runs/detect/experiments/E003A"
SUBMISSION_DIR = "submission"

def main():
    print("Exporting metrics and weights to submission directory...")
    os.makedirs(SUBMISSION_DIR, exist_ok=True)
    
    # Files to export
    files_to_export = [
        os.path.join(E003A_RUN_DIR, "weights", "best.pt"),
        os.path.join(E003A_RUN_DIR, "results.csv"),
        os.path.join(E003A_RUN_DIR, "BoxPR_curve.png"),
        os.path.join(E003A_RUN_DIR, "confusion_matrix.png")
    ]
    
    for fpath in files_to_export:
        if os.path.exists(fpath):
            fname = os.path.basename(fpath)
            shutil.copy(fpath, os.path.join(SUBMISSION_DIR, fname))
            print(f"Copied {fname}")
        else:
            print(f"Warning: {fpath} not found.")
            
if __name__ == "__main__":
    main()

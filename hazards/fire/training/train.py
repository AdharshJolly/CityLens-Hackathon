import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from ultralytics import YOLO
from shared.utilities.config_loader import load_config
from shared.utilities.logger import get_logger

logger = get_logger("FireTraining")

def train_model():
    logger.info("Starting Fire Hazard Training Pipeline")
    config = load_config('hazards/fire/configs/training.yaml')
    dataset = 'hazards/fire/configs/dataset.yaml'
    
    model = YOLO(config['model'])
    
    logger.info(f"Training Config: {config}")
    
    # DO NOT EXECUTE IN THIS PHASE
    # model.train(
    #     data=dataset,
    #     epochs=config['epochs'],
    #     imgsz=config['imgsz'],
    #     batch=config['batch'],
    #     patience=config['patience'],
    #     amp=config['amp'],
    #     workers=config['workers'],
    #     project=config['project'],
    #     name=config['name'],
    #     save_period=config['save_period']
    # )

if __name__ == "__main__":
    train_model()

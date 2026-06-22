from dataclasses import dataclass
from typing import List

@dataclass
class Detection:
    frame_id: int
    timestamp: float
    class_name: str
    confidence: float
    bbox: List[float]  # [x, y, w, h]

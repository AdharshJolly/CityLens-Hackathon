
from typing import List
from shared.contracts.detection import Detection

class YOLOAdapter:
    def __init__(self, class_mapping=None):
        self.class_mapping = class_mapping or {0: "fire", 1: "smoke"}

    def adapt(self, results, frame_id, timestamp) -> List[Detection]:
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                
                # normalized xywh [x_center, y_center, width, height]
                xywhn = box.xywhn[0].tolist()
                
                class_name = self.class_mapping.get(cls_id, "unknown")
                
                det = Detection(
                    frame_id=frame_id,
                    timestamp=timestamp,
                    class_name=class_name,
                    confidence=conf,
                    bbox=xywhn
                )
                detections.append(det)
        return detections

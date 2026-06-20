from typing import List
from shared.contracts.detection import Detection


class YOLOAdapter:
    def __init__(self, class_mapping=None):
        self.class_mapping = class_mapping or {
            0: "accident",
            1: "pedestrian_hazard"
        }

    def adapt(self, results, frame_id, timestamp) -> List[Detection]:
        """
        Converts raw YOLO output tensors into clean Detection domain objects.
        """
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id     = int(box.cls[0].item())
                conf       = float(box.conf[0].item())
                xywhn      = box.xywhn[0].tolist()  # normalized [x_center, y_center, w, h]
                class_name = self.class_mapping.get(cls_id, "unknown")

                detections.append(Detection(
                    frame_id=frame_id,
                    timestamp=timestamp,
                    class_name=class_name,
                    confidence=conf,
                    bbox=xywhn
                ))
        return detections

class Detection:
    def __init__(self, class_name, bbox, confidence):
        self.class_name = class_name
        self.bbox = bbox
        self.confidence = confidence


def adapt(results):
    detections = []

    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])
            bbox = box.xywh[0].tolist()

            detections.append(
                Detection(
                    class_name="streetlight",
                    bbox=bbox,
                    confidence=conf
                )
            )

    return detections

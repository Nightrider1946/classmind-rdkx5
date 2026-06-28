import sys

from .config import MODEL_ZOO, YOLO_MODEL

# Add Model Zoo paths
sys.path.append(MODEL_ZOO)
sys.path.append(
    MODEL_ZOO + "/samples/vision/ultralytics_yolo/runtime/python"
)

from ultralytics_yolo_det import (
    UltralyticsYOLODetect,
    UltralyticsYOLODetectConfig,
)


class YOLODetector:

    def __init__(self):

        cfg = UltralyticsYOLODetectConfig(
            model_path=YOLO_MODEL
        )

        self.model = UltralyticsYOLODetect(cfg)

    def detect_people(self, frame):

        boxes, scores, cls_ids = self.model.predict(frame)

        persons = []

        for box, score, cls_id in zip(boxes, scores, cls_ids):

            # COCO class 0 = Person
            if cls_id == 0 and score > 0.6:

                x1, y1, x2, y2 = map(int, box)

                crop = frame[y1:y2, x1:x2]

                persons.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": float(score),
                    "crop": crop
                })

        return persons
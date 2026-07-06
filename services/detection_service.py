from dataclasses import dataclass

import easyocr
import numpy as np
from ultralytics import YOLO

from Utils.data_utils import preprocess_detection_data

YOLO_MODEL = "awcr_system_best_model.pt"
DETECTION_CONFIDENCE_THRESHOLD = 0.55
LICENCE_PLATE_CLASS_ID = 0


@dataclass
class Detection:
    """
    A single license plate detected in a camera frame.

    Attributes:
        plate_text (str): The license plate text read by OCR.
        confidence (float): The detection confidence in range 0-1.
        box (tuple): The bounding box coordinates as (x1, y1, x2, y2).
    """
    plate_text: str
    confidence: float
    box: tuple[int, int, int, int]


class DetectionService:
    def __init__(self, model: YOLO, reader: easyocr.Reader):
        self.model = model
        self.reader = reader

    @classmethod
    def create(cls) -> "DetectionService":
        """
        Creates the service with the production YOLO model and OCR reader.

        Returns:
            DetectionService: A service instance ready to process frames.
        """
        return cls(model=YOLO(YOLO_MODEL), reader=easyocr.Reader(["en"]))

    def process_frame(self, frame: np.ndarray) -> list[Detection]:
        """
        Detects licence plates in the given frame and reads their text.

        Args:
            frame (np.ndarray): A single camera frame in RGB format.

        Returns:
            list[Detection]: One Detection per licence plate found in the frame.
        """
        detections = []
        results = self.model(frame)

        for result in results:
            for box in result.boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                if class_id != LICENCE_PLATE_CLASS_ID or confidence <= DETECTION_CONFIDENCE_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                plate_roi = frame[y1:y2, x1:x2]

                ocr_result = self.reader.readtext(plate_roi, detail=0)
                plate_text = preprocess_detection_data(ocr_result)

                detections.append(
                    Detection(
                        plate_text=plate_text,
                        confidence=confidence,
                        box=(x1, y1, x2, y2)
                    )
                )
        return detections

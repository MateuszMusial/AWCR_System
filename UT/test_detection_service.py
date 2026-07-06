from unittest.mock import MagicMock

import numpy as np
import pytest
from pytest_mock import MockerFixture

from services.detection_service import DetectionService


@pytest.fixture
def fake_frame() -> np.ndarray:
    """Fixture to create a small black RGB frame."""
    return np.zeros((100, 100, 3), dtype=np.uint8)


def make_fake_yolo_result(confidence: float, class_id: int, coords: tuple[int, int, int, int]) -> MagicMock:
    """Build a fake YOLO result with a single detection box."""
    box = MagicMock()
    box.conf = [confidence]
    box.cls = [class_id]
    box.xyxy = [coords]

    result = MagicMock()
    result.boxes = [box]
    return result


def test_process_frame_detects_plate(fake_frame: np.ndarray) -> None:
    """
    Test whether a confident licence plate box produces a Detection with OCR text.
    """
    # Arrange
    model = MagicMock(return_value=[make_fake_yolo_result(0.9, 0, (10, 20, 30, 40))])
    reader = MagicMock()
    reader.readtext.return_value = ["test 123"]
    service = DetectionService(model, reader)

    # Act
    detections = service.process_frame(fake_frame)

    # Assert
    assert len(detections) == 1
    assert detections[0].plate_text == "TEST123"
    assert detections[0].confidence == 0.9
    assert detections[0].box == (10, 20, 30, 40)


@pytest.mark.parametrize(
    "confidence, class_id",
    [
        pytest.param(
            0.2,
            0,
            id="Confidence below threshold"
        ),
        pytest.param(
            0.9,
            1,
            id="Wrong class id"
        )
    ]
)
def test_process_frame_filters_out_box(fake_frame: np.ndarray, confidence: float, class_id: int) -> None:
    """
    Test whether boxes below the confidence threshold or with a wrong class are filtered out.
    """
    # Arrange
    model = MagicMock(return_value=[make_fake_yolo_result(confidence, class_id, (10, 20, 30, 40))])
    reader = MagicMock()
    service = DetectionService(model, reader)

    # Act
    detections = service.process_frame(fake_frame)

    # Assert
    assert detections == []
    reader.readtext.assert_not_called()


def test_process_frame_no_boxes_returns_empty_list(fake_frame: np.ndarray) -> None:
    """
    Test whether a frame without any detected boxes produces an empty list.
    """
    # Arrange
    model = MagicMock(return_value=[])
    reader = MagicMock()
    service = DetectionService(model, reader)

    # Act
    detections = service.process_frame(fake_frame)

    # Assert
    assert detections == []


def test_create_loads_production_model(mocker: MockerFixture) -> None:
    """
    Test whether the factory builds the service with the production model and reader.
    """
    # Arrange
    mocked_yolo = mocker.patch("services.detection_service.YOLO")
    mocked_reader = mocker.patch("services.detection_service.easyocr.Reader")

    # Act
    service = DetectionService.create()

    # Assert
    mocked_yolo.assert_called_once_with("awcr_system_best_model.pt")
    mocked_reader.assert_called_once_with(["en"])
    assert service.model is mocked_yolo.return_value
    assert service.reader is mocked_reader.return_value

from unittest.mock import MagicMock

import numpy as np
import pytest
from pytest_mock import MockerFixture

from services.camera_service import CameraService, CAMERA_WIDTH, CAMERA_HEIGHT, FPS_VALUE


@pytest.fixture
def mocked_cv2(mocker: MockerFixture) -> MagicMock:
    """Fixture to patch cv2 in the camera service module."""
    return mocker.patch("services.camera_service.cv2")


def test_open_camera_configures_camera(mocked_cv2: MagicMock) -> None:
    """
    Test whether opening the camera sets the resolution and FPS and returns True.
    """
    # Arrange
    mocked_cv2.VideoCapture.return_value.isOpened.return_value = True
    service = CameraService()

    # Act
    result = service.open_camera()

    # Assert
    assert result is True
    service.camera.set.assert_any_call(mocked_cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    service.camera.set.assert_any_call(mocked_cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    service.camera.set.assert_any_call(mocked_cv2.CAP_PROP_FPS, FPS_VALUE)


def test_open_camera_failure_returns_false(mocked_cv2: MagicMock) -> None:
    """
    Test whether a camera that cannot be opened is not configured and returns False.
    """
    # Arrange
    mocked_cv2.VideoCapture.return_value.isOpened.return_value = False
    service = CameraService()

    # Act
    result = service.open_camera()

    # Assert
    assert result is False
    service.camera.set.assert_not_called()


def test_open_camera_uses_directshow_backend_on_windows(mocked_cv2: MagicMock, mocker: MockerFixture) -> None:
    """
    Test whether the DirectShow backend is used on Windows.
    """
    # Arrange
    mocker.patch("services.camera_service.sys.platform", "win32")
    service = CameraService()

    # Act
    service.open_camera()

    # Assert
    mocked_cv2.VideoCapture.assert_called_once_with(0, mocked_cv2.CAP_DSHOW)


def test_open_camera_uses_default_backend_on_other_platforms(mocked_cv2: MagicMock, mocker: MockerFixture) -> None:
    """
    Test whether the default backend is used on non-Windows platforms.
    """
    # Arrange
    mocker.patch("services.camera_service.sys.platform", "linux")
    service = CameraService()

    # Act
    service.open_camera()

    # Assert
    mocked_cv2.VideoCapture.assert_called_once_with(0)


def test_read_frame_returns_rgb_frame(mocked_cv2: MagicMock) -> None:
    """
    Test whether a successfully read frame is converted to RGB and returned.
    """
    # Arrange
    bgr_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    rgb_frame = np.ones((100, 100, 3), dtype=np.uint8)
    mocked_cv2.cvtColor.return_value = rgb_frame

    service = CameraService()
    service.camera = MagicMock()
    service.camera.isOpened.return_value = True
    service.camera.read.return_value = (True, bgr_frame)

    # Act
    frame = service.read_frame()

    # Assert
    assert frame is rgb_frame
    mocked_cv2.cvtColor.assert_called_once_with(bgr_frame, mocked_cv2.COLOR_BGR2RGB)


def test_read_frame_failed_read_returns_none(mocked_cv2: MagicMock) -> None:
    """
    Test whether a failed camera read produces None instead of a frame.
    """
    # Arrange
    service = CameraService()
    service.camera = MagicMock()
    service.camera.isOpened.return_value = True
    service.camera.read.return_value = (False, None)

    # Act
    frame = service.read_frame()

    # Assert
    assert frame is None
    mocked_cv2.cvtColor.assert_not_called()


def test_read_frame_camera_not_opened_returns_none(mocked_cv2: MagicMock) -> None:
    """
    Test whether reading from a never opened camera produces None.
    """
    # Arrange
    service = CameraService()

    # Act
    frame = service.read_frame()

    # Assert
    assert frame is None


def test_release_camera_releases_capture() -> None:
    """
    Test whether releasing the camera delegates to the capture device.
    """
    # Arrange
    service = CameraService()
    service.camera = MagicMock()

    # Act
    service.release_camera()

    # Assert
    service.camera.release.assert_called_once()


def test_release_camera_safe_when_never_opened() -> None:
    """
    Test whether releasing a never opened camera does not raise an error.
    """
    # Arrange
    service = CameraService()

    # Act & Assert - should not raise
    service.release_camera()

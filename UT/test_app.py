from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from Database.DBHandler import DBHandler
from GUI.app import GuiHandler
from services.detection_service import DetectionService
from email_handler import EmailHandler


@pytest.fixture()
def gui_handler() -> GuiHandler:
    """Fixture to create a GuiHandler instance."""
    return GuiHandler(EmailHandler(), DBHandler(), DetectionService.create())


def test_set_window_common_parts(gui_handler: GuiHandler, mocker: MockerFixture) -> None:
    """
    Test the set_window_common_parts method of GuiHandler.
    """
    # Arrange
    mocker = mocker.patch('tkinter.PhotoImage', return_value="awcrLogo.png")
    gui_handler.window = MagicMock()

    # Act
    gui_handler.set_window_common_parts("test")

    # Assert
    mocker.assert_called_once_with(file="awcrLogo.png")
    gui_handler.window.title.assert_called_once_with("test")
    gui_handler.window.geometry.assert_called_once_with("800x550")
    gui_handler.window.iconphoto.assert_called_once_with(True, gui_handler.icon)
    assert gui_handler.window.columnconfigure.call_count == 2


def test_create_window(gui_handler: GuiHandler, mocker: MockerFixture) -> None:
    """
    Test the create_window method of GuiHandler.
    """
    # Arrange
    mock_tk_instance = MagicMock()
    mock_tk_instance.title.return_value = "Test_window_name"

    mocker_tk = mocker.patch('GUI.app.Tk', return_value=mock_tk_instance)
    mocker.patch('GUI.app.Style')
    logger_mock = mocker.patch('GUI.app.awcr_logger.debug')

    # Act
    gui_handler.create_window("Test_window_name")

    # Assert
    assert gui_handler.window is not None
    mocker_tk.assert_called_once()
    gui_handler.window.title.assert_has_calls([
        mocker.call("Test_window_name"),
        mocker.call()
    ])
    logger_mock.assert_called_once_with('Created Test_window_name window successfully!')


def test_is_alert_on_cooldown(gui_handler: GuiHandler, mocker: MockerFixture) -> None:
    """
    Test whether repeated alerts for the same licence plate are suppressed
    during the cooldown period and allowed again after it expires.
    """
    # Arrange
    mocker.patch('GUI.app.time.monotonic', side_effect=[0.0, 30.0, 100.0])

    # Act
    first_alert = gui_handler._is_alert_on_cooldown("WA2137PL")
    second_alert = gui_handler._is_alert_on_cooldown("WA2137PL")
    third_alert = gui_handler._is_alert_on_cooldown("WA2137PL")

    # Assert
    assert first_alert is False
    assert second_alert is True
    assert third_alert is False


def test_is_alert_on_cooldown_independent_plates(gui_handler: GuiHandler, mocker: MockerFixture) -> None:
    """
    Test whether the cooldown of one licence plate does not affect another plate.
    """
    # Arrange
    mocker.patch('GUI.app.time.monotonic', side_effect=[0.0, 10.0])

    # Act
    first_plate_alert = gui_handler._is_alert_on_cooldown("WA2137PL")
    second_plate_alert = gui_handler._is_alert_on_cooldown("KR12345")

    # Assert
    assert first_plate_alert is False
    assert second_plate_alert is False

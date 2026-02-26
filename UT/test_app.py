from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from Database.DBHandler import DBHandler
from GUI.app import GuiHandler
from email_handler import EmailHandler


@pytest.fixture()
def gui_handler() -> GuiHandler:
    """Fixture to create a GuiHandler instance."""
    return GuiHandler(EmailHandler(), DBHandler())


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

import logging
from pytest_mock import MockerFixture

from logger import create_log_directory, get_logger, LOGS_DIRECTORY


def test_create_log_directory(mocker: MockerFixture) -> None:
    """
    Test whether function creates logs directory correctly.
    """
    # Arrange
    mocked_makedirs = mocker.patch("os.makedirs")

    # Act
    create_log_directory()

    # Assert
    mocked_makedirs.assert_called_once_with(LOGS_DIRECTORY)


def test_get_logger() -> None:
    """
    Test whether logger instance is created properly.
    """
    test_logger = get_logger("test_logger")

    assert isinstance(test_logger, logging.Logger)
    assert test_logger.name == "test_logger"

import pytest
from unittest.mock import patch

from Utils.common import display_detection_info, is_valid_email


@patch("Utils.common.messagebox.showwarning")
@patch("Utils.common.awcr_logger.info")
def test_displays_message_box_with_correct_info(mock_logger_info, mock_messagebox):
    brand = "Toyota"
    model = "Corolla"
    licence_plate = "ABC123"

    display_detection_info(brand, model, licence_plate)

    mock_logger_info.assert_called_once_with(
        "Detected wanted car Toyota Corolla with ABC123 licence plate!"
    )
    mock_messagebox.assert_called_once_with(
        "Wanted car detected!\n",
        "Detected wanted car Toyota Corolla\nwith ABC123 licence plate!"
    )


@patch("Utils.common.messagebox.showwarning", side_effect=Exception("Messagebox error"))
@patch("Utils.common.awcr_logger.info")
def test_handles_messagebox_error_gracefully(mock_logger_info, mock_messagebox):
    brand = "Ford"
    model = "Focus"
    licence_plate = "XYZ789"

    with pytest.raises(Exception, match="Messagebox error"):
        display_detection_info(brand, model, licence_plate)

    mock_logger_info.assert_called_once_with(
        "Detected wanted car Ford Focus with XYZ789 licence plate!"
    )

    mock_messagebox.assert_called_once_with(
        "Wanted car detected!\n",
        "Detected wanted car Ford Focus\n"
        "with XYZ789 licence plate!"
    )


@pytest.mark.parametrize(
    "email, expected_result",
    [
        pytest.param(
            "user@example.com",
            True,
            id="Valid email"
        ),
        pytest.param(
            "first.last+tag@sub.domain.org",
            True,
            id="Valid email with dots and plus"
        ),
        pytest.param(
            "",
            False,
            id="Empty email"
        ),
        pytest.param(
            "no-at-sign.com",
            False,
            id="Missing @ character"
        ),
        pytest.param(
            "user@domain",
            False,
            id="Missing top level domain"
        ),
        pytest.param(
            "user name@example.com",
            False,
            id="Whitespace in email"
        ),
        pytest.param(
            "user@@example.com",
            False,
            id="Double @ character"
        )
    ]
)
def test_is_valid_email(email: str, expected_result: bool) -> None:
    """
    Test whether email format validation behaves correctly.
    """
    # Arrange
    # Act
    result = is_valid_email(email)

    # Assert
    assert isinstance(result, bool)
    assert result is expected_result

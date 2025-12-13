import pytest
from unittest.mock import patch

from Utils.common import display_detection_info


@patch("Utils.common.messagebox.showwarning")
@patch("Utils.common.logger.info")
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
@patch("Utils.common.logger.info")
def test_handles_messagebox_error_gracefully(mock_logger_info, mock_messagebox):
    brand = "Ford"
    model = "Focus"
    licence_plate = "XYZ789"

    with pytest.raises(Exception, match="Messagebox error"):
        display_detection_info(brand, model, licence_plate)

    mock_logger_info.assert_called_once_with(
        "Detected wanted car Ford Focus with XYZ789 licence plate!"
    )

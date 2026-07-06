import re
from tkinter import messagebox

import logger


awcr_logger = logger.get_logger(__name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """
    Check if the given string looks like a valid email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email has a valid format, False otherwise.
    """
    return bool(EMAIL_PATTERN.match(email))


def display_detection_info(brand: str, model: str, licence_plate: str) -> None:
    """
    Display a message box with the detected wanted car information.
    Args:
        brand (str): The brand of the car.
        model (str): The model of the car.
        licence_plate (str): The license plate of the car.
    """
    awcr_logger.info(f"Detected wanted car {brand} {model} with {licence_plate} licence plate!")

    messagebox.showwarning(
        "Wanted car detected!\n",
        f"Detected wanted car {brand} {model}\n"
        f"with {licence_plate} licence plate!"
    )

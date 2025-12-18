from tkinter import messagebox

import logger


logger = logger.get_logger("Common utils logger")


def display_detection_info(brand: str, model: str, licence_plate: str) -> None:
    """
    Display a message box with the detected wanted car information.
    Args:
        brand (str): The brand of the car.
        model (str): The model of the car.
        licence_plate (str): The license plate of the car.
    """
    logger.info(f"Detected wanted car {brand} {model} with {licence_plate} licence plate!")

    messagebox.showwarning(
        "Wanted car detected!\n",
        f"Detected wanted car {brand} {model}\n"
        f"with {licence_plate} licence plate!"
    )

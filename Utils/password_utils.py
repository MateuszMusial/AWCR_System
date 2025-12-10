import bcrypt

import logger
from typing import Any

logger = logger.get_logger("password_utils logger")


def hash_password(password: str) -> str:
    """Function to encrypt plain text password provided by user."""
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(password.encode(encoding="utf-8"), salt)
    return encrypted_password.decode(encoding="utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided password matches the hashed password.

    Args:
        password (str): The plaintext password provided by the user in the GUI.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def validate_password_strength(password_to_validate: str) -> tuple[bool, Any] | tuple[bool, str]:
    """
    Function to check if password meets the minimum requirements.
    """
    if len(password_to_validate) < 8:
        return False, "Password too short!"

    password_requirements = {
        "small_letter": 0,
        "capital_letter": 0,
        "number": 0,
        "special_character": 0,
    }

    for char in password_to_validate:
        if char.islower():
            password_requirements["small_letter"] += 1
        elif char.isupper():
            password_requirements["capital_letter"] += 1
        elif char.isdigit():
            password_requirements["number"] += 1
        elif not char.isalnum():
            password_requirements["special_character"] += 1

    if all(value >= 1 for value in password_requirements.values()):
        return True, None
    else:
        return False, "Weak password! Please use number, small and capital letter and special character."


def get_password_from_file(path: str = "secret.txt") -> str:
    """
    Function to read password from file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(f"Cannot find'{path}'file.")
        raise RuntimeError(f"Cannot find'{path}'file.")

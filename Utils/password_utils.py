import bcrypt


def hash_password(password: str) -> str:
    """Function to encrypt plain text password provided by user."""
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(password.encode(), salt)
    return encrypted_password.decode()


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

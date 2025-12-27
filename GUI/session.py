from dataclasses import dataclass

import logger

awcr_logger = logger.get_logger("password_utils logger")


@dataclass
class Session:
    """
    A class to represent a user session.

    Attributes:
        email_address (str): The email address associated with the current session.
    """
    email_address: str = ""

    def assign_current_user(self, email: str) -> None:
        """
        Assigns the email address of the current user to the session.

        Args:
            email (str): The email address to assign to the session.
        """
        if not email or "@" not in email:
            raise ValueError(f"Invalid email address: {email}")
        self.email_address = email
        awcr_logger.info(f"Assigning email '{email}' to the session.")

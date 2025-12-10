import smtplib
import logger
from email.message import EmailMessage

from Utils.password_utils import get_password_from_file

logger = logger.get_logger("email logger")

AWCR_SYSTEM_EMAIL = 'systemawcr@gmail.com'
PASSWORD = get_password_from_file()


class EmailHandler:
    def __init__(self, user: str):
        self.logged_user = user
        self.host = "smtp.gmail.com"
        self.port = 587

    def send_detected_car_information_email(self, detection: str) -> None:
        """
        Send email to the user with the information about detected car.
        Args:
            detection (str): String containing information about the detected car.
        """
        msg = EmailMessage()
        msg['Subject'] = 'AWCR System detection report.'
        msg['From'] = AWCR_SYSTEM_EMAIL
        msg['To'] = self.logged_user

        body = (
            "Detection Report:\n\n"
            f"{detection}\n\n"
            "Best regards,\n"
            "AWCR Team"
        )
        msg.set_content(body)

        with smtplib.SMTP(self.host, port=587) as connection:
            connection.starttls()
            connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
            connection.send_message(msg)

        logger.info(f"Sending detection email to {self.logged_user}")

    def send_user_registered_information_email(self) -> None:
        """
        Send email to the user with the information about successful registration.
        """
        msg = EmailMessage()
        msg['Subject'] = 'Welcome to AWCR System!'
        msg['From'] = AWCR_SYSTEM_EMAIL
        msg['To'] = self.logged_user

        body = (
            "Hello,\n\n"
            "You are successfully registered to AWCR System!\n\n"
            "Best regards,\n"
            "AWCR Team"
        )
        msg.set_content(body)

        with smtplib.SMTP(self.host, port=587) as connection:
            connection.starttls()
            connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
            connection.send_message(msg)

        logger.info(f"Sending registration email to {self.logged_user}")

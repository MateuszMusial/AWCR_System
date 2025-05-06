import smtplib
import logger

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

        with smtplib.SMTP(self.host, port=587) as connection:
            connection.starttls()
            connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=AWCR_SYSTEM_EMAIL,
                to_addrs=self.logged_user,
                msg=detection)

        logger.info(f"Sending detection email to {self.logged_user}")

    def send_user_registered_information_email(self) -> None:
        """
        Send email to the user with the information about successful registration.
        """

        with smtplib.SMTP(self.host, port=587) as connection:
            connection.starttls()
            connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=AWCR_SYSTEM_EMAIL,
                to_addrs=self.logged_user,
                msg="You are successfully registered to AWCR System!"
            )

        logger.info(f"Sending registration email to {self.logged_user}")

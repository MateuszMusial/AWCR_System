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

    def send_detected_car_information_email(self, *, brand: str, model: str, licence_plate: str) -> None:
        """
        Send email to the user with the information about a detected car.
        This method accepts only keyword arguments.
        Args:
            brand (str): The brand of the detected car.
            model (str): The model of the detected car.
            licence_plate (str): The licence plate of the detected car.
        """
        msg = EmailMessage()
        msg['Subject'] = 'AWCR System detection report.'
        msg['From'] = AWCR_SYSTEM_EMAIL
        msg['To'] = self.logged_user

        body = (
            "Detection Report:\n\n"
            "Wanted car decetcted!\n"
            f"Detected wanted car {brand} {model}\n"
            f"with {licence_plate} licence plate!\n\n"
            "Best regards,\n"
            "AWCR Team"
        )
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.host, port=587) as connection:
                connection.starttls()
                connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
                connection.send_message(msg)
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email: {e}")

        logger.info(f"Sending detection email to {self.logged_user}")

    def send_user_registered_information_email(self) -> None:
        """
        Send email to the user with the information about successful registration.
        """
        msg = EmailMessage()
        msg['Subject'] = 'Welcome to AWCR System!'
        msg['From'] = AWCR_SYSTEM_EMAIL
        msg['To'] = self.logged_user

        image_path = 'awcrLogo.png'

        body_html = """
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>🎉 Congratulations!</h2>
                <p>Your account in the AWCR system has been successfully created.</p>

                <h3>What you can do now:</h3>
                <ul>
                    <li>✓ Monitor vehicles on your watchlist</li>
                    <li>✓ Receive notifications about detected cars</li>
                    <li>✓ Manage detections data</li>
                </ul>

                <p>Best regards,<br><strong>AWCR Team</strong></p>
                <img src="cid:awcrLogo" alt="AWCR Logo" style="width: 150px; margin-bottom: 20px;">
            </body>
        </html>
        """

        msg.set_content(body_html, subtype='html')

        if image_path:
            try:
                with open(image_path, 'rb') as attachment:
                    file_data = attachment.read()
                    msg.add_related(
                        file_data,
                        maintype='image',
                        subtype='png',
                        cid='awcrLogo'
                    )
            except FileNotFoundError:
                logger.error(f"Logo image not found at {image_path}")

        try:
            with smtplib.SMTP(self.host, port=587) as connection:
                connection.starttls()
                connection.login(user=AWCR_SYSTEM_EMAIL, password=PASSWORD)
                connection.send_message(msg)
                logger.info(f"Sending registration email to {self.logged_user}")
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email: {e}")

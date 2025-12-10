import sqlite3
from datetime import datetime, timedelta

from logger import get_logger
from Utils.password_utils import check_password, hash_password

logger = get_logger()


class DBHandler:
    def __init__(self):
        self.db_name = "awcr_database"

    def user_login(self, user_email: str, user_password: str) -> bool:
        """
        Check if user is in the database and password is correct.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM Users WHERE email = (?) ", (user_email, ))
            result = cursor.fetchone()

        if result:
            return check_password(user_password, result[0])
        return False

    def add_user(self, email: str, password: str) -> tuple[bool, str]:
        """
        Add user to the database.
        """
        hashed_password = hash_password(password)

        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)",
                                (email, hashed_password))
                connection.commit()
                logger.info(f"User {email} successfully registered to AWCR System!")
        except sqlite3.IntegrityError:
            logger.error("User already exist in the AWCR System!")
            return False, "User already exist in the AWCR System!"

        return True, f"User {email} successfully registered to AWCR System!"

    def fetch_detections_data(self, period: str) -> list[tuple]:
        """Fetch data based on period."""
        now = datetime.now()

        match period:
            case "Today":
                days_ago = now - timedelta(days=1)
            case "Last week":
                days_ago = now - timedelta(days=7)
            case "Last month":
                days_ago = now - timedelta(days=30)
            case "Last year":
                days_ago = now - timedelta(days=365)
            case _:
                logger.error("Unrecognized time period!")
                return []

        timestamp_str = days_ago.strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (timestamp_str,))
            return cursor.fetchall()

    def check_detected_car_in_database(self, final_result: str) -> tuple[bool, tuple | None]:
        """
        Check if the detected car is already in the database.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Cars WHERE license_plate = (?)", (final_result,))
            result = cursor.fetchone()
            if result:
                return True, result
        return False, None

    def add_detection(self, licence_plate: str) -> None:
        """
        Add detection to the database.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Detections (license_plate, timestamp) VALUES (?, datetime('now'))",
                           (licence_plate,))
            connection.commit()
            logger.info(f"Added detection of car with licence plate {licence_plate} to the database.")

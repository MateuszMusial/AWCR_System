import sqlite3
from contextlib import closing
from datetime import datetime, timedelta

from logger import get_logger
from Utils.password_utils import check_password, hash_password

awcr_logger = get_logger(__name__)


class DBHandler:
    def __init__(self, db_name: str = "awcr_database"):
        self.db_name = db_name

    def user_login(self, user_email: str, user_password: str) -> bool:
        """
        Check if user is in the database and password is correct.
        """
        with closing(sqlite3.connect(self.db_name)) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM Users WHERE email = ?", (user_email,))
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
            with closing(sqlite3.connect(self.db_name)) as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)",
                               (email, hashed_password))
                connection.commit()
                awcr_logger.info(f"User {email} successfully registered to AWCR System!")
        except sqlite3.IntegrityError:
            awcr_logger.error("User already exists in the AWCR System!")
            return False, "User already exists in the AWCR System!"

        return True, f"User {email} successfully registered to AWCR System!"

    def fetch_detections_data(self, period: str) -> list[tuple]:
        """Fetch data based on period."""
        now = datetime.now()

        match period:
            case "Today":
                since = now.replace(hour=0, minute=0, second=0, microsecond=0)
            case "Last week":
                since = now - timedelta(days=7)
            case "Last month":
                since = now - timedelta(days=30)
            case "Last year":
                since = now - timedelta(days=365)
            case _:
                awcr_logger.error("Unrecognized time period!")
                return []

        timestamp_str = since.strftime('%Y-%m-%d %H:%M:%S')

        with closing(sqlite3.connect(self.db_name)) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (timestamp_str,))
            return cursor.fetchall()

    def check_detected_car_in_database(self, final_result: str) -> tuple[bool, tuple | None]:
        """
        Check if the detected car is already in the database.
        """
        with closing(sqlite3.connect(self.db_name)) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Cars WHERE license_plate = ?", (final_result,))
            result = cursor.fetchone()
            if result:
                return True, result
        return False, None

    def add_detection(self, licence_plate: str) -> None:
        """
        Add detection to the database.
        """
        with closing(sqlite3.connect(self.db_name)) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM Cars WHERE license_plate = ?", (licence_plate,))
            car_id_result = cursor.fetchone()
            car_id = car_id_result[0] if car_id_result else None

            cursor.execute(
                "INSERT INTO Detections (license_plate, timestamp, car_id) "
                "VALUES (?, datetime('now', 'localtime'), ?)",
                (licence_plate, car_id))
            connection.commit()
            awcr_logger.info(f"Added detection of car with licence plate {licence_plate} to the database.")

import sqlite3
from datetime import datetime, timedelta

from logger import get_logger
from Utils.password_utils import check_password, hash_password

logger = get_logger()


class DBHandler:
    def __init__(self):
        self.db_name = "awcr_database"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def user_login(self, user_email: str, user_password: str) -> bool:
        """
        Check if user is in the database and password is correct.
        """
        self.cursor.execute("SELECT password FROM Users WHERE email = (?) ", (user_email, ))
        result = self.cursor.fetchone()

        if result:
            return check_password(user_password, result[0])
        return False

    def add_user(self, email: str, password: str) -> tuple[bool, str]:
        """
        Add user to the database.
        """
        hashed_password = hash_password(password)

        try:
            self.cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)",
                                (email, hashed_password))
            self.conn.commit()
            logger.info(f"User {email} successfully registered to AWCR System!")
        except sqlite3.IntegrityError:
            logger.error("User already exist in the AWCR System!")
            return False, "User already exist in the AWCR System!"

        return True, f"User {email} successfully registered to AWCR System!"

    def close_connection(self):
        self.conn.close()

    def fetch_detections_data(self, period: str) -> list[tuple]:
        """
        Fetch data from the database based on the specified period.
        """
        match period:
            case "Today":
                days_ago = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (days_ago,))
            case "Last week":
                days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (days_ago,))
            case "Last month":
                days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (days_ago,))
            case "Last year":
                days_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute("SELECT * FROM Detections WHERE timestamp >= ?", (days_ago,))
            case _:
                logger.error("Unrecognized time period!")
                return []

        data = self.cursor.fetchall()
        return data

    def check_detected_car_in_database(self, final_result):
        """
        Check if the detected car is already in the database.
        """
        self.cursor.execute("SELECT * FROM Cars WHERE license_plate = (?)", (final_result,))
        result = self.cursor.fetchone()
        if result:
            return True, result
        return False, None

    def add_detection(self, licence_plate):
        """
        Add detection to the database.
        """
        self.cursor.execute("INSERT INTO Detections (license_plate, timestamp) VALUES (?, datetime('now'))",
                            (licence_plate,))
        self.conn.commit()

    '''
    Script to create database structure.
    '''
    # def setup_database(self):
    #     self.cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         email TEXT NOT NULL UNIQUE,
    #         password TEXT NOT NULL
    #     );
    #     ''')
    #
    #     self.cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Cars (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         license_plate TEXT NOT NULL UNIQUE,
    #         brand TEXT,
    #         model TEXT,
    #         vin_number TEXT NOT NULL UNIQUE
    #         );
    #     ''')
    #
    #     self.cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Detections (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         license_plate TEXT NOT NULL,
    #         timestamp TEXT NOT NULL,
    #         car_id INTEGER,
    #         FOREIGN KEY (car_id) REFERENCES Cars(id)
    #     );
    #     ''')

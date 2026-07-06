import os
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from Database.DBHandler import DBHandler

SCHEMA_PATH = os.path.join("Database", "schema.sql")

USER_EMAIL = "test.user@example.com"
USER_PASSWORD = "Str0ng!Password"

WANTED_CAR = ("WA2137PL", "Skoda", "Superb", "VIN_SUPERB_2137")


@pytest.fixture()
def db_handler(tmp_path: Path) -> DBHandler:
    """Fixture to create a DBHandler instance backed by a temporary database."""
    db_path = str(tmp_path / "test_awcr_database")

    with closing(sqlite3.connect(db_path)) as connection:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            connection.executescript(schema_file.read())
        connection.execute(
            "INSERT INTO Cars (license_plate, brand, model, vin_number) VALUES (?, ?, ?, ?)",
            WANTED_CAR
        )
        connection.commit()

    return DBHandler(db_path)


def test_add_user(db_handler: DBHandler) -> None:
    """
    Test whether a new user is added to the database correctly.
    """
    # Arrange
    # Act
    result, message = db_handler.add_user(USER_EMAIL, USER_PASSWORD)

    # Assert
    assert result is True
    assert message == f"User {USER_EMAIL} successfully registered to AWCR System!"


def test_add_user_already_exists(db_handler: DBHandler) -> None:
    """
    Test whether adding the same user twice is rejected.
    """
    # Arrange
    db_handler.add_user(USER_EMAIL, USER_PASSWORD)

    # Act
    result, message = db_handler.add_user(USER_EMAIL, USER_PASSWORD)

    # Assert
    assert result is False
    assert message == "User already exists in the AWCR System!"


def test_add_user_stores_hashed_password(db_handler: DBHandler) -> None:
    """
    Test whether the password is stored hashed, not in plain text.
    """
    # Arrange
    db_handler.add_user(USER_EMAIL, USER_PASSWORD)

    # Act
    with closing(sqlite3.connect(db_handler.db_name)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM Users WHERE email = ?", (USER_EMAIL,))
        stored_password = cursor.fetchone()[0]

    # Assert
    assert stored_password != USER_PASSWORD
    assert stored_password.startswith("$2b$")


@pytest.mark.parametrize(
    "login_email, login_password, expected_result",
    [
        pytest.param(
            USER_EMAIL,
            USER_PASSWORD,
            True,
            id="Correct credentials"
        ),
        pytest.param(
            USER_EMAIL,
            "WrongPassword1!",
            False,
            id="Wrong password"
        ),
        pytest.param(
            "unknown.user@example.com",
            USER_PASSWORD,
            False,
            id="Unknown user"
        )
    ]
)
def test_user_login(db_handler: DBHandler, login_email: str, login_password: str, expected_result: bool) -> None:
    """
    Test whether user login is verified correctly against the database.
    """
    # Arrange
    db_handler.add_user(USER_EMAIL, USER_PASSWORD)

    # Act
    result = db_handler.user_login(login_email, login_password)

    # Assert
    assert isinstance(result, bool)
    assert result is expected_result


def test_check_detected_car_in_database_found(db_handler: DBHandler) -> None:
    """
    Test whether a wanted car is found in the database by its licence plate.
    """
    # Arrange
    # Act
    car_is_wanted, details = db_handler.check_detected_car_in_database("WA2137PL")

    # Assert
    assert car_is_wanted is True
    assert details is not None
    _, licence_plate, brand, model, _ = details
    assert (licence_plate, brand, model) == ("WA2137PL", "Skoda", "Superb")


def test_check_detected_car_in_database_not_found(db_handler: DBHandler) -> None:
    """
    Test whether an unknown licence plate is reported as not wanted.
    """
    # Arrange
    # Act
    car_is_wanted, details = db_handler.check_detected_car_in_database("XX00000")

    # Assert
    assert car_is_wanted is False
    assert details is None


def test_add_detection_links_known_car(db_handler: DBHandler) -> None:
    """
    Test whether a detection of a known car is stored with its car id.
    """
    # Arrange
    # Act
    db_handler.add_detection("WA2137PL")

    # Assert
    with closing(sqlite3.connect(db_handler.db_name)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT license_plate, timestamp, car_id FROM Detections")
        licence_plate, timestamp, car_id = cursor.fetchone()

    assert licence_plate == "WA2137PL"
    assert timestamp is not None
    assert car_id == 1


def test_fetch_detections_data_returns_recent_detection(db_handler: DBHandler) -> None:
    """
    Test whether a freshly added detection is returned for every period.
    """
    # Arrange
    db_handler.add_detection("WA2137PL")

    # Act
    result = db_handler.fetch_detections_data("Today")

    # Assert
    assert len(result) == 1
    assert result[0][1] == "WA2137PL"


def test_fetch_detections_data_excludes_old_detection(db_handler: DBHandler) -> None:
    """
    Test whether detections older than the requested period are filtered out.
    """
    # Arrange
    with closing(sqlite3.connect(db_handler.db_name)) as connection:
        connection.execute(
            "INSERT INTO Detections (license_plate, timestamp, car_id) VALUES (?, ?, ?)",
            ("WA2137PL", "2020-01-01 10:00:00", 1)
        )
        connection.commit()

    # Act
    result = db_handler.fetch_detections_data("Last week")

    # Assert
    assert result == []


def test_fetch_detections_data_unrecognized_period(db_handler: DBHandler) -> None:
    """
    Test whether an unrecognized period returns an empty list.
    """
    # Arrange
    db_handler.add_detection("WA2137PL")

    # Act
    result = db_handler.fetch_detections_data("Last decade")

    # Assert
    assert result == []

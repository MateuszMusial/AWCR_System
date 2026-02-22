import sqlite3
import os
from logger import get_logger, setup_logger

setup_logger()
logger = get_logger("init_db")

DB_NAME = "awcr_database"
SCHEMA_PATH = os.path.join("Database", "schema.sql")


def create_and_populate_db():
    if os.path.exists(DB_NAME):
        logger.info(f"Database '{DB_NAME}' already exists. Skipping initialization.")
        return

    logger.info(f"Database '{DB_NAME}' not found. Creating new database...")

    if not os.path.exists(SCHEMA_PATH):
        logger.error(f"Error: Schema file not found at '{SCHEMA_PATH}'.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
            cursor.executescript(schema)

        logger.info("Tables created successfully.")

        cars_data = [
            ("WA2137PL", "Skoda", "Superb", "VIN_SUPERB_2137"),
            ("KR12345", "Toyota", "Corolla", "VIN_TOYOTA_12345"),
            ("GD67890", "Ford", "Focus", "VIN_FORD_67890"),
            ("PO54321", "Volkswagen", "Passat", "VIN_VW_54321")
        ]

        logger.info("Inserting sample cars...")
        cursor.executemany(
            "INSERT INTO Cars (license_plate, brand, model, vin_number) VALUES (?, ?, ?, ?)",
            cars_data
        )
        conn.commit()
        logger.info(f"Database '{DB_NAME}' initialized with {len(cars_data)} sample cars.")

    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_and_populate_db()

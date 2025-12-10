from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import logger

logger = logger.get_logger("Data utils logger")

WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class Period(Enum):
    TODAY = "Today"
    LAST_WEEK = "Last week"
    LAST_MONTH = "Last month"
    LAST_YEAR = "Last year"


def preprocess_detection_data(ocr_result: list[str]) -> str:
    """
    Processes the result from OCR to extract the license plate number.
    """
    if not ocr_result:
        return ""

    if len(ocr_result) > 1:
        one_result = "".join(ocr_result)
        return one_result.strip().replace(" ", "").upper()
    return ocr_result[0].strip().replace(" ", "").upper()


def prepare_detection_data_for_plot(data: list[tuple], period: str) -> dict[str, int]:
    """
    Processes the detection data for plotting.
    Args:
        data: Detection data from the database.
        period: Time period for which the data is fetched.
                Accepted values: "Today", "Last week", "Last month", "Last year"

    Returns:
        dict: Keys as labels (e.g., days/months), values as counts.
    """
    logger.debug(f"Processing detection data for period: {period}")

    if not data:
        logger.error("No detection data provided.")
        return {}

    try:
        df = pd.DataFrame(data, columns=['id', 'license_plate', 'detection_time', 'car_id'])
        df['detection_time'] = pd.to_datetime(df['detection_time'])
    except (ValueError, KeyError) as e:
        logger.error(f"Failed to parse detection data: {e}")
        return {}

    now = datetime.now()

    match period:
        case "Today":
            today = now.date()
            df = df[df['detection_time'].dt.date == today]
            result = {str(today): len(df)}

        case "Last week":
            week_ago = now - timedelta(days=7)
            df = df[df['detection_time'] >= week_ago]
            df['weekday'] = df['detection_time'].dt.day_name().str[:3]
            counts = df['weekday'].value_counts().to_dict()
            result = {day: counts.get(day, 0) for day in WEEKDAYS}

        case "Last month":
            month_ago = now - timedelta(days=30)
            df = df[df['detection_time'] >= month_ago]
            df['day'] = df['detection_time'].dt.day
            result = df['day'].value_counts().sort_index().to_dict()

        case "Last year":
            year_ago = now - timedelta(days=365)
            df = df[df['detection_time'] >= year_ago]
            df['month'] = df['detection_time'].dt.month_name().str[:3]
            counts = df['month'].value_counts().to_dict()
            result = {month: counts.get(month, 0) for month in MONTHS}

        case _:
            logger.error(f"Unknown period: {period}")
            return {}
    return result


def export_detection_data_to_csv(data: list[tuple]) -> None:
    """
    Exports the detection data to a CSV file.
    Args:
        data: Detection data from the database.
    """
    if not data:
        logger.error("No detection data to export.")
        return

    try:
        df = pd.DataFrame(data, columns=['id', 'license_plate', 'detection_time', 'car_id'])
        df['detection_time'] = pd.to_datetime(df['detection_time'])

        filename = f"detections_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Detection data exported to {filename}")
    except (ValueError, IOError) as e:
        logger.error(f"Failed to export detection data: {e}")

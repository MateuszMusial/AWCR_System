from datetime import datetime, timedelta
import pandas as pd

import logger


logger = logger.get_logger("Data utils logger")


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


def prepare_detection_data_for_plot(data, period: str) -> dict:
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

    df = pd.DataFrame(data, columns=['id', 'license_plate', 'detection_time', 'car_id'])
    df['detection_time'] = pd.to_datetime(df['detection_time'])

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
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            counts = df['weekday'].value_counts().to_dict()
            result = {day: counts.get(day, 0) for day in weekdays}

        case "Last month":
            month_ago = now - timedelta(days=30)
            df = df[df['detection_time'] >= month_ago]
            df['day'] = df['detection_time'].dt.day
            result = df['day'].value_counts().sort_index().to_dict()

        case "Last year":
            year_ago = now - timedelta(days=365)
            df = df[df['detection_time'] >= year_ago]

            df['month'] = df['detection_time'].dt.month_name().str[:3]

            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            counts = df['month'].value_counts().to_dict()
            result = {month: counts.get(month, 0) for month in months}

        case _:
            logger.error(f"Unknown period: {period}")
            return {}

    return result

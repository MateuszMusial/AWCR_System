from datetime import datetime, timedelta

import pytest

from Utils.data_utils import preprocess_detection_data, prepare_detection_data_for_plot, WEEKDAYS


@pytest.mark.parametrize(
    "ocr_result, expected_output",
    [
        pytest.param(
            [],
            "",
            id="Empty list"
        ),
        pytest.param(
            ["ABC123"],
            "ABC123",
            id="Single item list"
        ),
        pytest.param(
            ["ABC", "123"],
            "ABC123",
            id="Multiple items list"
        ),
        pytest.param(
            ["  abc  ", "  123  "],
            "ABC123",
            id="Leading and trailing spaces"
        ),
        pytest.param(
            ["a bc", " def"],
            "ABCDEF",
            id="Multiple items with spaces"
        )
    ]
)
def test_preprocess_detection_data(ocr_result: list[str], expected_output: str) -> None:
    """
    Test the preprocess_detection_data function.
    """
    # Arrange
    # Act
    result = preprocess_detection_data(ocr_result)

    # Assert
    assert isinstance(result, str)
    assert result == expected_output


@pytest.mark.parametrize(
    "data, period",
    [
        pytest.param(
            [],
            "Last week",
            id="Empty data"
        ),
        pytest.param(
            [(1, "WA2137PL", "2025-06-12 10:00:00", 1)],
            "Last decade",
            id="Unknown period"
        ),
        pytest.param(
            [(1, "WA2137PL", "not a timestamp", 1)],
            "Last week",
            id="Invalid timestamp"
        )
    ]
)
def test_prepare_detection_data_for_plot_invalid_input(data: list[tuple], period: str) -> None:
    """
    Test whether invalid input to prepare_detection_data_for_plot returns an empty dict.
    """
    # Arrange
    # Act
    result = prepare_detection_data_for_plot(data, period)

    # Assert
    assert result == {}


def test_prepare_detection_data_for_plot_last_week() -> None:
    """
    Test whether detections from the last week are counted per weekday.
    """
    # Arrange
    yesterday = datetime.now() - timedelta(days=1)
    timestamp = yesterday.strftime('%Y-%m-%d %H:%M:%S')
    data = [
        (1, "WA2137PL", timestamp, 1),
        (2, "KR12345", timestamp, 2)
    ]
    expected_weekday = yesterday.strftime('%a')

    # Act
    result = prepare_detection_data_for_plot(data, "Last week")

    # Assert
    assert list(result.keys()) == WEEKDAYS
    assert result[expected_weekday] == 2
    assert sum(result.values()) == 2


def test_prepare_detection_data_for_plot_today() -> None:
    """
    Test whether today's detections are counted under today's date.
    """
    # Arrange
    now = datetime.now()
    data = [(1, "WA2137PL", now.strftime('%Y-%m-%d %H:%M:%S'), 1)]

    # Act
    result = prepare_detection_data_for_plot(data, "Today")

    # Assert
    assert result == {str(now.date()): 1}

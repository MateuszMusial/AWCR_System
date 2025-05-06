import pytest

from Utils.data_utils import preprocess_detection_data


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

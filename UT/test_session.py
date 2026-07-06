import pytest

from GUI.session import Session


def test_assign_current_user() -> None:
    """
    Test whether a valid email is assigned to the session.
    """
    # Arrange
    session = Session()

    # Act
    session.assign_current_user("user@example.com")

    # Assert
    assert session.email_address == "user@example.com"


@pytest.mark.parametrize(
    "invalid_email",
    [
        pytest.param(
            "",
            id="Empty email"
        ),
        pytest.param(
            "no-at-sign.com",
            id="Missing @ character"
        )
    ]
)
def test_assign_current_user_invalid_email(invalid_email: str) -> None:
    """
    Test whether an invalid email is rejected with ValueError.
    """
    # Arrange
    session = Session()

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email address"):
        session.assign_current_user(invalid_email)

    assert session.email_address == ""

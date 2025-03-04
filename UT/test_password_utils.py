import pytest

from Utils.password_utils import hash_password, check_password, validate_password_strength


@pytest.mark.parametrize(
    "plain_text_password",
    [
        pytest.param(
            "",
            id="Empty password"
        ),
        pytest.param(
            "1234",
            id="Simple password"
        ),
        pytest.param(
            "Ksdv@#119873KSA!",
            id="Strong password"
        )
    ]
)
def test_hash_password(plain_text_password) -> None:
    """
    Test whether password is hashed correctly.
    """
    # Arrange
    # Act
    hashed_password = hash_password(plain_text_password)

    # Assert
    assert isinstance(hashed_password, str)
    assert hashed_password.startswith("$2b$")
    assert hashed_password != plain_text_password


@pytest.mark.parametrize(
    "plain_text_password, expected_password",
    [
        pytest.param(
            "",
            "$2b$12$NzXsIbbISerbRZso3csinOByYZ9J51SboIuRPR4m/fHcl6hYk136e",
            id="Empty password"
        ),
        pytest.param(
            "1234",
            "$2b$12$M9GINUTLoHWzYuoP4mBTmuSLJflSjg5aRsNxWp1l04fYx//r//8G.",
            id="Simple password"
        ),
        pytest.param(
            "Ksdv@#119873KSA!",
            "$2b$12$PUmZpKXFUfVF7QYYLcCqW.8/FjmQvwVHnt9Wnif5GMhfH01it6iZS",
            id="Strong password"
        )
    ]
)
def test_verify_password(plain_text_password, expected_password) -> None:
    """
    Test whether password is verified correctly.
    Tests with correct data.
    """
    # Arrange
    # Act
    result = check_password(plain_text_password, expected_password)

    # Assert
    assert isinstance(result, bool)
    assert result is True


@pytest.mark.parametrize(
    "plain_text_password, expected_password",
    [
        pytest.param(
            "$2b$12$pcpCaXrBdQgcPiv",
            "$2b$12$pcpCaXrBdQgcPivO/Dom7undqbZVgfAsDtIATJF8JxbYl6HUUtvdy",
            id="Simple hashed password"
        ),
        pytest.param(
            "",
            "$2b$12$pcpCaXrBdQgcPivO/Dom7undqbZVgfAsDtIATJF8JxbYl6HUUtvdy",
            id="Empty password"
        )
    ]
)
def test_verify_password_incorrect_data(plain_text_password, expected_password) -> None:
    """
    Test whether password is verified correctly.
    Tests with incorrect data.
    """
    # Arrange
    # Act
    result = check_password(plain_text_password, expected_password)

    # Assert
    assert isinstance(result, bool)
    assert result is False


@pytest.mark.parametrize(
    "plain_text_password, expected_result",
    [
        pytest.param(
            "short",
            (False, "Password too short!"),
            id="Too short password hashed password"
        ),
        pytest.param(
            "",
            (False, "Password too short!"),
            id="Empty password"
        ),
        pytest.param(
            "aB12!!jjjaaaa6465NSJJ",
            True,
            id="Correct password"
        ),
        pytest.param(
            "weakPassword",
            (False, "Weak password! Please use number, small and capital letter and special character."),
            id="Weak password"
        ),
        pytest.param(
            "weakPassword134111",
            (False, "Weak password! Please use number, small and capital letter and special character."),
            id="Weak password with numbers"
        )
    ]
)
def test_validate_password_strength(plain_text_password, expected_result) -> None:
    """
    Check whether function validate_password_strength behaves correctly
    Args:
        plain_text_password: Plain text password from GUI
        expected_result: Boolean value or tuple(bool, str)

    Returns:
        None
    """
    # Assert
    assert validate_password_strength(plain_text_password) == expected_result

import pytest

@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("abc@example.com", "abc123", 200),  # Valid credentials
        ("abc2@example.com", "abc123", 200),  # Valid credentials
        ("abc@example.com", "abc1234", 401),  # Incorrect password
        ("nonexistent@example.com", "password", 404),  # Non-existent user
    ],
)
def test_login(client, test_user_admin, test_user, email, password, status_code):
    response = client.post(
        "/login/", data={"username": email, "password": password}
    )

    assert response.status_code == status_code

    if status_code == 200:
        assert "access_token" in response.json()
    else:
        assert "detail" in response.json()

import pytest

def test_successful_login(client, test_users):
    data = {
        "email": "abc@example.com",
        "password": "abc123"
    }
    res = client.post('/login/', data = data)
    print(res)
    assert res.status_code == 200
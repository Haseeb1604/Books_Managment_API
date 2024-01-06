import pytest

@pytest.mark.parametrize("name, email, password, usertype", [
    ("abc", "abc@gmail.com", "1234", "normal"),
    ("haseeb", "haseeb@gmail.com", "1234", "admin"),
    ("haseeb", "abc2@gmail.com", "1234", "normal"),
])
def test_create_users(client, name, email, password, usertype):
    """
    User Data for creating
        name: str
        email: EmailStr
        usertype: Optional[str] = "normal"
        password: str
    """
    data = {
        "name": name,
        "email": email,
        "usertype": usertype,
        "password": password
    }
    res = client.post('/users/', json = data)
    assert res.status_code == 200

def test_create_users_with_usertype_default(client):
    data = {
        "name": "abc",
        "email": "abc@example.com",
        "password": "abc123"
    }
    res = client.post("/users/", json=data)
    assert res.status_code == 200

def test_create_users_with_email_exist(client, test_users):
    data = {
        "name": "abc",
        "email": "abc@example.com",
        "password": "abc123"
    }
    res = client.post("/users/", json=data)
    assert res.status_code == 409
import pytest

# Creating User
@pytest.mark.parametrize(
    "user_data, expected_status_code",
    [
        ({"name": "abc", "email": "abc@gmail.com", "password": "1234", "usertype": "normal"}, 201),
        ({"name": "haseeb", "email": "haseeb@gmail.com", "password": "1234", "usertype": "admin"}, 201),
        ({"name": "haseeb", "email": "abc3@gmail.com", "password": "1234", "usertype": "normal"}, 201),
        ({"name": "abc", "email": "abc2@example.com", "password": "abc123"}, 409),  # Existing email
        ({"email": "abc@example.com", "password": "abc123"}, 422),  # Missing fields
    ]
)
def test_create_users(client, test_user, user_data, expected_status_code):
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == expected_status_code
    
    if res.status_code == 422:
        assert res.json()["detail"][0]["type"] == "missing"


@pytest.mark.parametrize(
    # test_user_admin ID = 1
    # test_user       ID = 2
    "client_fixture, user_id, expected_status_code",
    [
        ("authorized_client", 1, 200), #admin retriving his data
        ("authorized_client_normal", 2, 200), #normal user retriving his data
        ("authorized_client_normal", 1, 403), #normal user retriving others data
        ("client", None, 401), # unauthorized client retriving all data
        ("client", 1, 401), # unauthorized client retriving one user data
        ("authorized_client", None, 200), # unauthorized client retriving all data
        ("authorized_client_normal", None, 403), # normal user retriving all data
        ("authorized_client", 999, 404), # retriving data not exists
    ]
)
def test_get_users(client_fixture, user_id, expected_status_code, request, test_user_admin, test_user):
    client = request.getfixturevalue(client_fixture)

    if user_id is not None:
        url = f"/users/{user_id}"
    else:
        url = "/users/"

    res = client.get(url)

    assert res.status_code == expected_status_code

@pytest.mark.parametrize(
    "client_fixture, user_id, expected_status_code",
    [
        ("authorized_client", "user_id", 204), #admin deleting user
        ("authorized_client_normal", "user_id", 204), #normal user deleting his/her own account
        ("authorized_client_normal", "user_id_admin", 403), #normal user deleting other
        ("client", "user_id_admin", 401), #unautherized client deleting user
        ("authorized_client", 999, 404), #authorized client deleting user not exist
    ]
)
def test_delete_user(client_fixture, user_id, expected_status_code, request, test_user_admin, test_user):
    client = request.getfixturevalue(client_fixture)

    if user_id == "user_id":
        url = f"/users/{test_user['id']}"
    elif user_id == "user_id_admin":
        url = f"/users/{test_user_admin['id']}"
    else:
        url = f"/users/{user_id}"

    res = client.delete(url)
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    "client_fixture, user_id, data, expected_status_code",
    [
        ("authorized_client", "test_user_id", {"name": "abc1234", "email": "abc1234@example.com", "password": "abc123", "userType": "normal"}, 201), #admin updating user data
        ("authorized_client_normal", "test_user_admin_id", {"name": "abc1234", "email": "abc1234@example.com", "password": "abc123", "userType": "normal"}, 403), # normal user updating other data
        ("client", "test_user_admin_id", {"name": "abc1234", "email": "abc1234@example.com", "password": "abc123", "userType": "normal"}, 401), # unauthorized client updating data
        ("authorized_client", 9999, {"name": "abc1234", "email": "abc1234@example.com", "password": "abc123", "userType": "normal"}, 404), # Non existent user update
    ]
)
def test_update_user(client_fixture, user_id, data, expected_status_code, request, test_user, test_user_admin):
    client = request.getfixturevalue(client_fixture)

    if user_id == "test_user_id":
        url = f"/users/{test_user['id']}"
    elif user_id == "test_user_admin_id":
        url = f"/users/{test_user_admin['id']}"
    else:
        url = f"/users/{user_id}"

    res = client.put(url, json=data)
    assert res.status_code == expected_status_code

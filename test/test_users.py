import pytest

# # Creating User
# @pytest.mark.parametrize(
#     "user_data, expected_status_code",
#     [
#         ({"name": "abc", "email": "abc@gmail.com", "password": "1234", "usertype": "normal"}, 201),
#         ({"name": "haseeb", "email": "haseeb@gmail.com", "password": "1234", "usertype": "admin"}, 201),
#         ({"name": "haseeb", "email": "abc3@gmail.com", "password": "1234", "usertype": "normal"}, 201),
#         ({"name": "abc", "email": "abc2@example.com", "password": "abc123"}, 409),  # Existing email
#         ({"email": "abc@example.com", "password": "abc123"}, 422),  # Missing fields
#     ]
# )
# def test_create_users(client, test_user, user_data, expected_status_code):
#     res = client.post("/users/", json=user_data)
    
#     assert res.status_code == expected_status_code
    
#     if res.status_code == 422:
#         assert res.json()["detail"][0]["type"] == "missing"



import pytest

# test_user_admin ID = 1
# test_user       ID = 2

@pytest.mark.parametrize(
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

# def test_delete_user_by_admin(authorized_client, test_user_admin, test_user):
#     res = authorized_client.delete(f"/users/{test_user['id']}")
#     assert res.status_code == 204

# def test_delete_user_by_normal_user(authorized_client_normal, test_user_admin, test_user):
#     res = authorized_client_normal.delete(f"/users/{test_user_admin['id']}")
#     assert res.status_code == 403

# def test_delete_user_by_unauthorized(client, test_user_admin, test_user):
#     res = client.delete(f"/users/{test_user_admin['id']}")
#     assert res.status_code == 401

# def test_delete_user_not_exist(authorized_client, test_user_admin, test_user):
#     res = authorized_client.delete("/users/999")
#     assert res.status_code == 404

# def test_update_user_by_admin(authorized_client, test_user, test_user_admin):
#     data = {
#         "name": "abc1234",
#         "email": "abc1234@example.com",
#         "password": "abc123",
#         "userType": "normal"
#     }
#     res = authorized_client.put(f"/users/{test_user['id']}", json=data)
#     assert res.status_code == 201

# def test_update_other_user_by_normal_user(authorized_client_normal, test_user, test_user_admin):
#     data = {
#         "name": "abc1234",
#         "email": "abc1234@example.com",
#         "password": "abc123",
#         "userType": "normal"
#     }
#     res = authorized_client_normal.put(f"/users/{test_user_admin['id']}", json=data)
#     assert res.status_code == 403

# def test_update_other_user_by_unauthorized(client, test_user, test_user_admin):
#     data = {
#         "name": "abc1234",
#         "email": "abc1234@example.com",
#         "password": "abc123",
#         "userType": "normal"
#     }
#     res = client.put(f"/users/{test_user_admin['id']}", json=data)
#     assert res.status_code == 401

# def test_update_non_existing_user(authorized_client, test_user, test_user_admin):
#     data = {
#         "name": "abc1234",
#         "email": "abc1234@example.com",
#         "password": "abc123",
#         "userType": "normal"
#     }
#     res = authorized_client.put(f"/users/9999", json=data)
#     assert res.status_code == 404
import pytest

# @pytest.mark.parametrize("name, email, password, usertype", [
#     ("abc", "abc@gmail.com", "1234", "normal"),
#     ("haseeb", "haseeb@gmail.com", "1234", "admin"),
#     ("haseeb", "abc2@gmail.com", "1234", "normal"),
# ])
# def test_create_users(client, name, email, password, usertype):
#     data = {
#         "name": name,
#         "email": email,
#         "usertype": usertype,
#         "password": password
#     }
#     res = client.post('/users/', json = data)
#     assert res.status_code == 201

# def test_create_users_with_usertype_default(client):
#     data = {
#         "name": "abc",
#         "email": "abc@example.com",
#         "password": "abc123"
#     }
#     res = client.post("/users/", json=data)
#     assert res.status_code == 201

# def test_create_users_with_email_exist(client, test_user):
#     data = {
#         "name": "abc",
#         "email": "abc2@example.com",
#         "password": "abc123"
#     }
#     res = client.post("/users/", json=data)
#     assert res.status_code == 409

# def test_create_users_with_Null_fields(client):
#     data = {
#         "email": "abc@example.com",
#         "password": "abc123"
#     }
#     res = client.post("/users/", json=data)
#     assert res.status_code == 422
#     assert res.json()["detail"][0]["type"] == "missing"

# def test_get_all_users(authorized_client, test_user_admin, test_user):
#     res = authorized_client.get("/users/")
#     assert res.status_code == 200

# def test_get_all_users_normal_user(authorized_client_normal, test_user_admin, test_user):
#     res = authorized_client_normal.get("/users/")
#     assert res.status_code == 403

# def test_get_all_users_unautherized(client, test_user_admin, test_user):
#     res = client.get("/users/")
#     assert res.status_code == 401

# def test_get_one_user(authorized_client, test_user_admin, test_user):
#     res = authorized_client.get("/users/1")
#     assert res.status_code == 200

# def test_get_one_users_unautherized(client, test_user_admin, test_user):
#     res = client.get("/users/1")
#     assert res.status_code == 401

# def test_get_one_users_normal_user(authorized_client_normal, test_user_admin, test_user):
#     res = authorized_client_normal.get("/users/2")
#     assert res.status_code == 403

# def test_get_user_not_exist(authorized_client, test_user_admin, test_user):
#     res = authorized_client.get("/users/999")
#     assert res.status_code == 404

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

def test_update_user_by_admin(authorized_client, test_user, test_user_admin):
    data = {
        "name": "abc1234",
        "email": "abc1234@example.com",
        "password": "abc123",
        "userType": "normal"
    }
    res = authorized_client.put(f"/users/{test_user['id']}", json=data)
    assert res.status_code == 201

def test_update_other_user_by_normal_user(authorized_client_normal, test_user, test_user_admin):
    data = {
        "name": "abc1234",
        "email": "abc1234@example.com",
        "password": "abc123",
        "userType": "normal"
    }
    res = authorized_client_normal.put(f"/users/{test_user_admin['id']}", json=data)
    assert res.status_code == 403

def test_update_other_user_by_unauthorized(client, test_user, test_user_admin):
    data = {
        "name": "abc1234",
        "email": "abc1234@example.com",
        "password": "abc123",
        "userType": "normal"
    }
    res = client.put(f"/users/{test_user_admin['id']}", json=data)
    assert res.status_code == 401

def test_update_non_existing_user(authorized_client, test_user, test_user_admin):
    data = {
        "name": "abc1234",
        "email": "abc1234@example.com",
        "password": "abc123",
        "userType": "normal"
    }
    res = authorized_client.put(f"/users/9999", json=data)
    assert res.status_code == 404
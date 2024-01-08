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

def test_get_all_users(authorized_client, test_user_admin, test_user):
    res = authorized_client.get("/users/")
    print(res.json())
    assert res.status_code == 200

# def test_delete_users(client, test_users):
#     res = client.delete(f"/users/{test_users[0].id}")
#     assert res.status_code == 204

# def test_update_users(client, test_users):
#     data = {
#         "name": "abc1234",
#         "email": "abc1234@example.com",
#         "password": "abc123",
#         "userType": "admin"
#     }
#     res = client.put(f"/users/{test_users[0].id}", json=data)
#     assert res.status_code == 201
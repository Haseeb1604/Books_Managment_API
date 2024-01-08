import pytest

# Test Cases for Publisher Creation
@pytest.mark.parametrize("client_fixture, publisher_data, expected_status_code", [
    ("authorized_client", {"name": "New Publisher 1"}, 201),  # Admin creating a new publisher
    ("authorized_client", {"name": "New Publisher 2"}, 201),  # Admin creating another new publisher
    ("authorized_client_normal", {"name": "New Publisher 3"}, 201),  # Normal user trying to create a publisher
    ("client", {"name": "New Publisher 4"}, 401),  # Unauthorized access to create a publisher
])
def test_create_publisher(client_fixture, publisher_data, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.post("/publisher/", json=publisher_data)
    assert res.status_code == expected_status_code

# Test Cases for Duplicate Publisher Creation
@pytest.mark.parametrize("client_fixture, publisher_data, expected_status_code", [
    ("authorized_client", {"name": "name 1"}, 409),  # Admin trying to create a publisher with existing name
    ("authorized_client_normal", {"name": "name 2"}, 409),  # Normal user trying to create a duplicate publisher
    ("client", {"name": "name 3"}, 401),  # Unauthorized access to create a duplicate publisher
])
def test_create_duplicate_publisher(client_fixture, test_publisher, publisher_data, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.post("/publisher/", json=publisher_data)
    assert res.status_code == expected_status_code

# Test Case for Reading All Publishers
@pytest.mark.parametrize("client_fixture, expected_status_code", [
    ("authorized_client", 200),  # Admin reading all publishers
    ("authorized_client_normal", 200),  # Normal user reading all publishers
    ("client", 200),  # Unauthorized access to read all publishers
])
def test_get_all_publishers(client_fixture, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.get("/publisher/")
    assert res.status_code == expected_status_code

# Test Case for Reading a Specific Publisher
@pytest.mark.parametrize("client_fixture, publisher_id, expected_status_code", [
    ("authorized_client", "test_publisher_id", 200),  # Admin reading a specific publisher
    ("client", 9999, 404),  # Reading a non-existing publisher
])
def test_get_publisher(client_fixture, publisher_id, expected_status_code, request, test_publisher):
    client = request.getfixturevalue(client_fixture)
    
    if publisher_id == "test_publisher_id":
        publisher_id = test_publisher[0].id
    
    res = client.get(f"/publisher/{publisher_id}")
    assert res.status_code == expected_status_code

# Test Cases for Publisher Deletion
@pytest.mark.parametrize("client_fixture, publisher_id, expected_status_code", [
    ("authorized_client", "test_publisher_id", 204),  # Admin deleting a specific publisher
    ("authorized_client_normal", "test_publisher_id", 403),  # Normal user trying to delete a publisher (Forbidden)
    ("client", "test_publisher_id", 401),  # Unauthorized access to delete a publisher
    ("authorized_client", 9999, 404),  # Deleting a non-existing publisher
])
def test_delete_publisher(client_fixture, publisher_id, expected_status_code, request, test_publisher, test_user_admin):
    client = request.getfixturevalue(client_fixture)
    
    if publisher_id == "test_publisher_id":
        publisher_id = test_publisher[0].id

    res = client.delete(f"/publisher/{publisher_id}")
    assert res.status_code == expected_status_code

# Test Cases for Publisher Update
@pytest.mark.parametrize("client_fixture, publisher_id, publisher_data, expected_status_code", [
    ("authorized_client", "test_publisher_id", {"name": "Updated Publisher 1"}, 201),  # Admin updating a specific publisher
    ("authorized_client_normal", "test_publisher_id", {"name": "Updated Publisher 2"}, 403),  # Normal user trying to update a publisher (Forbidden)
    ("client", "test_publisher_id", {"name": "Updated Publisher 3"}, 401),  # Unauthorized access to update a publisher
    ("authorized_client", 9999, {"name": "Updated Publisher 4"}, 404),  # Updating a non-existing publisher
])
def test_update_publisher(client_fixture, publisher_id, publisher_data, expected_status_code, request, test_publisher, test_user_admin):
    client = request.getfixturevalue(client_fixture)
    
    if publisher_id == "test_publisher_id":
        publisher_id = test_publisher[0].id

    res = client.put(f"/publisher/{publisher_id}", json=publisher_data)
    assert res.status_code == expected_status_code

import pytest

# Test Cases for Author Creation
@pytest.mark.parametrize("client_fixture, author_data, expected_status_code", [
    ("authorized_client", {"name": "New Author 1"}, 201),  # Admin creating a new author
    ("authorized_client", {"name": "New Author 2"}, 201),  # Admin creating another new author
    ("authorized_client_normal", {"name": "New Author 3"}, 201),  # Normal user trying to create an author
    ("client", {"name": "New Author 4"}, 401),  # Unauthorized access to create an author
])
def test_create_author(client_fixture, author_data, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.post("/author/", json=author_data)
    assert res.status_code == expected_status_code

# Test Cases for Duplicate Author Creation
@pytest.mark.parametrize("client_fixture, author_data, expected_status_code", [
    ("authorized_client", {"name": "name 1"}, 409),  # Admin trying to create an author with an existing name
    ("authorized_client_normal", {"name": "name 2"}, 409),  # Normal user trying to create a duplicate author
    ("client", {"name": "name 3"}, 401),  # Unauthorized access to create a duplicate author
])
def test_create_duplicate_author(client_fixture, test_author, author_data, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.post("/author/", json=author_data)
    assert res.status_code == expected_status_code

# Test Case for Reading All Authors
@pytest.mark.parametrize("client_fixture, expected_status_code", [
    ("authorized_client", 200),  # Admin reading all authors
    ("authorized_client_normal", 200),  # Normal user reading all authors
    ("client", 200),  # Unauthorized access to read all authors
])
def test_get_all_authors(client_fixture, expected_status_code, request):
    client = request.getfixturevalue(client_fixture)
    res = client.get("/author/")
    assert res.status_code == expected_status_code

# Test Case for Reading a Specific Author
@pytest.mark.parametrize("client_fixture, author_id, expected_status_code", [
    ("authorized_client", "test_author_id", 200),  # Admin reading a specific author
    ("client", 9999, 404),  # Reading a non-existing author
])
def test_get_author(client_fixture, author_id, expected_status_code, request, test_author):
    client = request.getfixturevalue(client_fixture)
    
    if author_id == "test_author_id":
        author_id = 1
    
    res = client.get(f"/author/{author_id}")
    assert res.status_code == expected_status_code

# Test Cases for Author Deletion
@pytest.mark.parametrize("client_fixture, author_id, expected_status_code", [
    ("authorized_client", "test_author_id", 204),  # Admin deleting a specific author
    ("authorized_client_normal", "test_author_id", 403),  # Normal user trying to delete an author (Forbidden)
    ("client", "test_author_id", 401),  # Unauthorized access to delete an author
    ("authorized_client", 9999, 404),  # Deleting a non-existing author
])
def test_delete_author(client_fixture, author_id, expected_status_code, request, test_author, test_user_admin):
    client = request.getfixturevalue(client_fixture)
    
    if author_id == "test_author_id":
        author_id = 1

    res = client.delete(f"/author/{author_id}")
    assert res.status_code == expected_status_code

# Test Cases for Author Update
@pytest.mark.parametrize("client_fixture, author_id, author_data, expected_status_code", [
    ("authorized_client", "test_author_id", {"name": "Updated Author 1"}, 201),  # Admin updating a specific author
    ("authorized_client_normal", "test_author_id", {"name": "Updated Author 2"}, 403),  # Normal user trying to update an author (Forbidden)
    ("client", "test_author_id", {"name": "Updated Author 3"}, 401),  # Unauthorized access to update an author
    ("authorized_client", 9999, {"name": "Updated Author 4"}, 404),  # Updating a non-existing author
])
def test_update_author(client_fixture, author_id, author_data, expected_status_code, request, test_author, test_user_admin):
    client = request.getfixturevalue(client_fixture)
    
    if author_id == "test_author_id":
        author_id = 1

    res = client.put(f"/author/{author_id}", json=author_data)
    assert res.status_code == expected_status_code

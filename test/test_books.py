import pytest

@pytest.mark.parametrize("book_id, expected_status_code", [
    (None, 200), # Reading all books
    (1, 200),  # Reading a specific book
    (9999, 404),  # Reading a non-existing book
])
def test_read_book(client, book_id, expected_status_code, test_books):
    if book_id:
        res = client.get(f"/books/{book_id}")
    else:
        res = client.get(f"/books/")
    assert res.status_code == expected_status_code

@pytest.mark.parametrize(
    "client_fixture, data, expected_status_code",
    [
        (
            "authorized_client", 
            {"title": "title 1", "price": 32, "auther_id": 1, "publisher_id": 2}, 
            201
        ), # Admin Creating new Book
        (
            "authorized_client_normal", 
            {"title": "title 2", "price": 12, "auther_id": 2, "publisher_id": 3}, 
            201
        ), # Normal user Creating new Book
        (
            "client", 
            {"title": "title 3", "price": 12, "auther_id": 2, "publisher_id": 3}, 
            401
        ), #unautherized client creating book
        (
            "authorized_client", 
            {"title": "title 5", "price": None, "auther_id": 2, "publisher_id": None}, 
            422
        ), #Missing Fields
    ]
)
def test_create_books(client_fixture, data, expected_status_code, request, test_user_admin, test_authers, test_publisher):
    client = request.getfixturevalue(client_fixture)
    res = client.post("/books/", json = data)
    assert res.status_code == expected_status_code

@pytest.mark.parametrize(
    "client_fixture, book_id, expected_status_code",
    [
        ("authorized_client", 1, 204),  # Admin deleting a book
        ("authorized_client_normal", 2, 204),  # Normal user deleting a book
        ("authorized_client_normal", 1, 403),  # Normal user deleting other book
        ("client", 1, 401),  # Unauthorized client attempting deletion
    ]
)
def test_delete_book(client_fixture, book_id, expected_status_code, request, test_books):
    client = request.getfixturevalue(client_fixture)
    res = client.delete(f"/books/{book_id}")
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    "client_fixture, book_id, data, expected_status_code",
    [
        (
            "authorized_client",
            1,
            {"title": "title 123", "price": 32, "auther_id": 2, "publisher_id": 3},
            200,
        ),  # Admin updating a book
        (
            "authorized_client_normal",
            2,
            {"title": "Updated Title", "price": 90, "auther_id": 2, "publisher_id": 1},
            200,
        ),  # Normal user updating a book
        (
            "authorized_client_normal",
            1,
            {"title": "Updated Title", "price": 90, "auther_id": 2, "publisher_id": 1},
            403,
        ),  # Normal user updating a other book
        (
            "client",
            1,
            {"title": "Updated Title", "price": 90, "auther_id": 2, "publisher_id": 1},
            401,
        ),  # Unauthorized client attempting update
        (
            "authorized_client",
            99999,
            {"title": "Updated Title", "price": 90, "auther_id": 2, "publisher_id": 1},
            404,
        ),  # Updating a non-existing book
        (
            "authorized_client",
            1,
            {"title": "Updated Title", "price": "90", "auther_id": None, "publisher_id": 1},
            422,
        ),  # Updating with invalid data type
    ]
)
def test_update_book(client_fixture, book_id, data, expected_status_code, request, test_books):
    client = request.getfixturevalue(client_fixture)
    res = client.put(f"/books/{book_id}", json=data)
    assert res.status_code == expected_status_code
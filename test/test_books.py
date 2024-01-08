import pytest

# @pytest.mark.parametrize("book_id, expected_status_code", [
#     (None, 200), # Reading all books
#     (1, 200),  # Reading a specific book
#     (9999, 404),  # Reading a non-existing book
# ])
# def test_read_book(client, book_id, expected_status_code, test_books):
#     if book_id:
#         res = client.get(f"/books/{book_id}")
#     else:
#         res = client.get(f"/books/")
#     assert res.status_code == expected_status_code


def test_create_books(test_user_admin, authorized_client, test_authers, test_publisher):
    res = authorized_client.post("/books/", json={
        "title": "title",
        "price": 12,
        "auther_id": 1,
        "publisher_id": 1
    })
    print(res.json())
    assert res.status_code == 201

# @pytest.mark.parametrize("title, price, auther, publisher",[
#     ("title 1", None, "auther 1", "publisher 1"),
#     ("title 2", 24, "auther 2", None),
#     ("title 3", 25, None, "publisher 3"),
# ])
# def test_create_books_with_missing_fields(client, title, price, auther, publisher):
#     res = client.post("/books/", json={
#         "title": title,
#         "price": price,
#         "auther": auther,
#         "publisher": publisher
#     })
#     assert res.status_code == 422

# def test_delete_book(client, test_books):
#     res = client.delete(f"/books/{test_books[0].id}")
#     assert res.status_code == 204

# def test_delete_book_not_defined(client, test_books):
#     res = client.delete(f"/books/99999")
#     assert res.status_code == 404

# def test_update_book(client, test_books):
#     data = {
#         "title": "title",
#         "price": 30,
#         "auther": "auther",
#         "publisher": "publisher"
#     }
#     res = client.put(f"/books/{test_books[0].id}", json = data)
#     assert res.status_code == 200

# def test_update_book_not_exist(client, test_books):
#     data = {
#         "title": "title",
#         "price": 30,
#         "auther": "auther",
#         "publisher": "publisher"
#     }
#     res = client.put(f"/books/99999", json = data)
#     assert res.status_code == 404

# def test_update_book_other_type(client, test_books):
#     data = {
#         "title": "title",
#         "price": "abc",
#         "auther": "auther",
#         "publisher": "publisher"
#     }
#     res = client.put(f"/books/{test_books[0].id}", json = data)
#     assert res.status_code == 422

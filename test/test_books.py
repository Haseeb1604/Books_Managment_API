import pytest

def test_get_all_posts(client, test_books):
    res = client.get("/books/")
    assert res.status_code == 200

def test_get_one_post(client, test_books):
    res = client.get(f"/books/{test_books[0].id}")
    assert res.status_code == 200

def test_get_undefined_post(client):
    res = client.get(f"/books/999999")
    assert res.status_code == 404

@pytest.mark.parametrize("title, price, auther, publisher",[
    ("title 1", 34, "auther 1", "publisher 1"),
    ("title 2", 24, "auther 2", "publisher 2"),
    ("title 3", 25, "auther 2", "publisher 3"),
])
def test_create_books(client, title, price, auther, publisher):
    res = client.post("/books/", json={
        "title": title,
        "price": price,
        "auther": auther,
        "publisher": publisher
    })
    assert res.status_code == 201

@pytest.mark.parametrize("title, price, auther, publisher",[
    ("title 1", None, "auther 1", "publisher 1"),
    ("title 2", 24, "auther 2", None),
    ("title 3", 25, None, "publisher 3"),
])
def test_create_books_with_missing_fields(client, title, price, auther, publisher):
    res = client.post("/books/", json={
        "title": title,
        "price": price,
        "auther": auther,
        "publisher": publisher
    })
    assert res.status_code == 422

def test_delete_book(client, test_books):
    res = client.delete(f"/books/{test_books[0].id}")
    assert res.status_code == 204

def test_delete_book_not_defined(client, test_books):
    res = client.delete(f"/books/99999")
    assert res.status_code == 404

def test_update_post(client, test_books):
    data = {
        "title": "title",
        "price": 30,
        "auther": "auther",
        "publisher": "publisher"
    }
    res = client.put(f"/books/{test_books[0].id}", json = data)
    assert res.status_code == 200

def test_update_post_not_exist(client, test_books):
    data = {
        "title": "title",
        "price": 30,
        "auther": "auther",
        "publisher": "publisher"
    }
    res = client.put(f"/books/99999", json = data)
    assert res.status_code == 404

def test_update_post_other_type(client, test_books):
    data = {
        "title": "title",
        "price": "abc",
        "auther": "auther",
        "publisher": "publisher"
    }
    res = client.put(f"/books/{test_books[0].id}", json = data)
    assert res.status_code == 422

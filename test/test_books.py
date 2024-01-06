import pytest

@pytest.mark.parametrize("title, price, auther, publisher",[
    ("title 1", 34, "auther 1", "publisher 1"),
    ("title 2", 24, "auther 2", "publisher 2"),
    ("title 3", 25, "auther 2", "publisher 3"),
])
def test_get_all_books(client, title, price, auther, publisher):
    res = client.post("/books/", json={
        "title": title,
        "price": price,
        "auther": auther,
        "publisher": publisher
    })
    assert res.status_code == 201
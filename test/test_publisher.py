import pytest

@pytest.mark.parametrize("name", ["name 1", "name 2", "name 3"])
def test_create_publisher(client, name):
    res = client.post("/publisher/", json={
        "name": name
    })
    assert res.status_code == 201

@pytest.mark.parametrize("name", ["name 1", "name 2", "name 3"])
def test_create_duplicate_publisher(client, test_publisher, name):
    res = client.post("/publisher/", json={
        "name": name
    })
    assert res.status_code == 409

def test_get_publisher(client, test_publisher):
    res = client.get(f"/publisher/{test_publisher[0].id}")
    assert res.status_code == 200

def test_get_wrong_publisher(client):
    res = client.get(f"/publisher/9999")
    assert res.status_code == 404

def test_get_all_publisher(client):
    res = client.get("/publisher/")
    assert res.status_code == 200
import pytest

@pytest.mark.parametrize("name", ["name 1", "name 2", "name 3"])
def test_create_auther(client, name):
    res = client.post("/auther/", json={
        "name": name
    })
    assert res.status_code == 201

@pytest.mark.parametrize("name", ["name 1", "name 2", "name 3"])
def test_create_duplicate_auther(client, test_authers):
    res = client.post("/auther/", json={
        "name": name
    })
    assert res.status_code == 409

def test_get_auther(client, test_authers):
    res = client.get(f"/auther/{test_authers[0].id}")
    assert res.status_code == 200

def test_get_wrong_auther(client):
    res = client.get(f"/auther/9999")
    assert res.status_code == 404

def test_get_all_authers(client):
    res = client.get("/auther/")
    assert res.status_code == 200
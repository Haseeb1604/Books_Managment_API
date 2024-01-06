import pytest

@pytest.mark.parametrize("name", ["name 1", "name 2", "name 3"])
def test_create_publisher(client, name):
    res = client.post("/publisher/", json={
        "name": name
    })
    assert res.status_code == 201


import pytest
from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
 
from app.config import settings
from app.Database import get_db
from app.Database import Base
from app import models

from app.routes import oauth2

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "name": "abc2",
        "email": "abc2@example.com",
        "password": "abc123",
        "usertype": "normal",
    }

    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert res.status_code == 201
    return new_user

@pytest.fixture
def test_user_admin(client):
    user_data = {
        "name": "abc",
        "email": "abc@example.com",
        "password": "abc123",
        "usertype": "admin",
    }

    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(test_user_admin):
    return oauth2.create_access_token({"user_id": test_user_admin["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

def add_model_to_db(session, Model, data):
    def create_model(auther):
        return Model(**auther)
    
    data_map = map(create_model, data)
    data_list = list(data_map)
    session.add_all(data_list)
    session.commit()
    data_list = session.query(Model).all()
    return data_list

@pytest.fixture
def test_authers(session):
    data = [{ "name": "name 1"},{"name": "name 2"},{"name": "name 3"}]
    return add_model_to_db(session, models.Auther, data)

@pytest.fixture
def test_publisher(session):
    data = [{ "name": "name 1"},{"name": "name 2"},{"name": "name 3"}]
    return add_model_to_db(session, models.Publisher, data)
    

@pytest.fixture
def test_books(session, test_user_admin, test_user, test_authers, test_publisher):
    data = [{
        "title": "first title",
        "price": 20,
        "auther_id": test_authers[0].id,
        "publisher_id": test_publisher[0].id,
        "owner_id": test_user_admin.id
    },{
        "title": "Second title",
        "price": 34,
        "auther_id": test_authers[2].id,
        "publisher_id": test_publisher[1].id,
        "owner_id": test_user.id
    },{
        "title": "third title",
        "price": 23,
        "auther_id": test_authers[1].id,
        "publisher_id": test_publisher[2].id,
        "owner_id": test_user.id
    }
    ]

    return add_model_to_db(session, models.Books, data)
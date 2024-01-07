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
def test_users(session):
    data = [{
        "name": "abc",
        "email": "abc@example.com",
        "password": "abc123",
        "usertype": "admin",
    },{
        "name": "abc123",
        "email": "abc123@example.com",
        "password": "1234",
        "usertype": "normal",
    },{
        "name": "user",
        "email": "user123@example.com",
        "password": "1234",
        "usertype": "normal",
    }
    ]

    return add_model_to_db(session, models.Users, data)
    

@pytest.fixture
def test_books(session, test_users):
    data = [{
        "title": "first title",
        "price": 12,
        "auther_id": 1,
        "publisher_id": 2,
        "owner_id": test_users[0].id
    },{
        "title": "Second title",
        "price": 34,
        "auther_id": 1,
        "publisher_id": 1,
        "owner_id": test_users[2].id
    },{
        "title": "third title",
        "price": 23,
        "auther_id": 2,
        "publisher_id": 2,
        "owner_id": test_users[1].id
    }
    ]

    return add_model_to_db(session, models.Books, data)
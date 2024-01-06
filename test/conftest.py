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

@pytest.fixture
def test_authers(session):
    data = [{ "name": "name 1"},{"name": "name 2"},{"name": "name 3"}]
    
    def create_auther_model(auther):
        return models.Auther(**auther)
    
    authers_map = map(create_auther_model, data)
    authers = list(authers_map)
    session.add_all(authers)
    session.commit()
    authers = session.query(models.Auther).all()
    return authers

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
    }
    ]

    def create_user_model(user):
        return models.Users(**user)

    users_map = map(create_user_model, data)
    users = list(users_map)
    session.add_all(users)
    session.commit()
    users = session.query(models.Users).all()
    return users
    

@pytest.fixture
def test_books(session):
    books_data = [{
        "title": "first title",
        "price": 12,
        "auther": "auther 1",
        "publisher": "publisher2 ",
    },{
        "title": "Second title",
        "price": 34,
        "auther": "auther 1",
        "publisher": "publisher 1",
    },{
        "title": "third title",
        "price": 23,
        "auther": "auther 2",
        "publisher": "publisher 1",
    }
    ]

    def create_book_model(book):
        return models.Books(**book)

    book_map = map(create_book_model, books_data)
    books = list(book_map)
    session.add_all(books)
    session.commit()
    books = session.query(models.Books).all()
    return books
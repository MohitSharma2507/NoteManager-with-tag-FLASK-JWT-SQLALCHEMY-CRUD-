import pytest
from app import createAapp, db
from config import TestingConfig


@pytest.fixture
def app():
    app = createAapp(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/signup", json={
        "email": "test@gmail.com",
        "password": "12345678"
    })

    login = client.post("/api/auth/login", json={
        "email": "test@gmail.com",
        "password": "12345678"
    })

    token = login.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
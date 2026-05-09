import pytest
from app import createAapp,db
     
#  @pytest.fixture means this function is a "setup helper".
#  Any test that writes app as a parameter gets this automatically — pytest injects it. You never call it yourself.

#  Create a test version of your app. TESTING=True shows real errors instead of hiding them. sqlite:///:memory: 
#  means use a temporary database in RAM — not your real notes.db file. Every test gets a fresh empty database.

# db.create_all() creates all tables before the test. yield app gives the app to the test — 
# the test runs here. db.drop_all() deletes everything after the test. So every test starts clean.

# 👉 Before yield → setup
# 👉 After yield → teardown
@pytest.fixture
def app():
    app = createAapp()
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        yield app  # Pauses here and returns app to client
        db.drop_all()


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

@pytest.fixture
def client(app):
    return app.test_client() #method of Flaskapp, creates test env/fake server to use method like client.get, client.posy eyc.
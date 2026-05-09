import pytest
@pytest.mark.order(1)
def test_signup(client):

    response = client.post("/api/auth/signup" , json={
        "email":"Mohit123@gmail.com",
        "password":"12345678"
    })

    print(response.json)  # 👈 you can see response here

    assert response.status_code == 201
    assert "message" in response.json

@pytest.mark.order(2)
def test_login(client):
    client.post('/api/auth/signup', json ={
       "email":"Mohit123@gmail.com",
        "password":"12345678"
    })   

    response = client.post("/api/auth/login", json={
        "email":"Mohit123@gmail.com",
        "password":"12345678"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data


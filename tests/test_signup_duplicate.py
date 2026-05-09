def test_signup_duplicate(client):
    client.post("/api/auth/signup", json={
        "email": "test@gmail.com",
        "password": "12345678"
    })

    response = client.post("/api/auth/signup", json={
        "email": "test@gmail.com",
        "password": "12345678"
    })

    assert response.status_code == 409
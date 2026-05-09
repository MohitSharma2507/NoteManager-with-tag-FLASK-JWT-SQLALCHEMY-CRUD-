def test_delete_note_unauthorized(client, auth_headers):
# create note with user 1
    create = client.post("/api/notes/add_note", json={
        "title": "Private", "content": "Mine"
    }, headers=auth_headers)
    note_id = create.get_json()["note"]["id"]

    # create user 2
    client.post("/api/auth/signup", json={
        "email": "user2@test.com", "password": "12345678"
    })
    login2 = client.post("/api/auth/login", json={
        "email": "user2@test.com", "password": "12345678"
    })
    headers2 = {"Authorization": f"Bearer {login2.get_json()['access_token']}"}

    # user 2 tries to delete user 1's note
    response = client.delete(f"/api/notes/delete_note/{note_id}",
                             headers=headers2)
    assert response.status_code == 403
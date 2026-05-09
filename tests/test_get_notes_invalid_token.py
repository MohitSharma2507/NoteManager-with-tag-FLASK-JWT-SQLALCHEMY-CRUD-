def test_get_notes_invalid_token(client):
    response = client.get(
        "/api/notes/get_notes",
        headers={"Authorization": "Bearer wrongtoken"}
    )

    assert response.status_code == 422
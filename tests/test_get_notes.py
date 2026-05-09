import pytest

@pytest.mark.order(5)
def test_get_notes(client, auth_headers):

    # create note first
    client.post("/api/notes/add_note", json={
        "title": "Note1",
        "content": "Content1"
    }, headers=auth_headers)

    response = client.get("/api/notes/get_notes", headers=auth_headers)

    data = response.get_json()

    assert response.status_code == 200
    assert "notes" in data
    assert isinstance(data["notes"], list)
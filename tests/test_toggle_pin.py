import pytest

@pytest.mark.order(7)
def test_toggle_pin(client, auth_headers):

    create = client.post("/api/notes/add_note", json={
        "title": "Pin Test",
        "content": "Testing pin"
    }, headers=auth_headers)

    note_id = create.get_json()["note"]["id"]

    response = client.patch(
        f"/api/notes/{note_id}/pin",
        headers=auth_headers
    )
    
    data = response.get_json()

    assert response.status_code == 200
    assert data["is_pinned"] is True
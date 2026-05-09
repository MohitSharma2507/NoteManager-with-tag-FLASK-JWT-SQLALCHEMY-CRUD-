import pytest

@pytest.mark.order(6)
def test_get_single_note(client, auth_headers):

    create = client.post("/api/notes/add_note", json={
        "title": "Single Note",
        "content": "Check this"
    }, headers=auth_headers)

    note_id = create.get_json()["note"]["id"]
    print(f"NoteId --------->>>>>> {note_id}" )

    response = client.get(f"/api/notes/get_note/{note_id}", headers=auth_headers)

    data = response.get_json()

    assert response.status_code == 200
    assert data["note"]["id"] == note_id
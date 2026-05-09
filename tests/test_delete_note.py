import pytest

@pytest.mark.order(10)
def test_delete_note(client, auth_headers):

    create = client.post("/api/notes/add_note", json={
        "title": "Delete Me",
        "content": "To be deleted"
    }, headers=auth_headers)

    note_id = create.get_json()["note"]["id"]
    print(f"NoteId --------->>>>>> {note_id}" )

    response = client.delete(
        f"/api/notes/delete_note/{note_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    # confirm deletion
    get_response = client.get(f"/api/notes/{note_id}", headers=auth_headers)
    assert get_response.status_code == 404
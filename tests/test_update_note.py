import pytest

@pytest.mark.order(9)
def test_update_note(client, auth_headers):

    create = client.post("/api/notes/add_note", json={
        "title": "Old Title",
        "content": "Old Content"
    }, headers=auth_headers)

    note_id = create.get_json()["note"]["id"]

    response = client.put(
        f"/api/notes/update_note/{note_id}",
        json={
            "title": "Updated",
            "content":"New Content",
            "tags": ["newtag1", "newtag2"]  
        },
        headers=auth_headers
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["note"]["title"] == "Updated"
    tag_names = [t["name"] for t in data["note"]["tags"]]
    assert "newtag1" in tag_names
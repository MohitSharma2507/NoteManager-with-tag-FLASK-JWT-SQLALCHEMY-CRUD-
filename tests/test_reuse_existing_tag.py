def test_reuse_existing_tag(client, auth_headers):
    # create first note with tag 'work'
    client.post("/api/notes/add_note", json={
        "title": "Note 1", "content": "First",
        "tags": ["work"]
    }, headers=auth_headers)

    # create second note with same tag 'work' — hits reuse branch (line 34)
    response = client.post("/api/notes/add_note", json={
        "title": "Note 2", "content": "Second",
        "tags": ["work"]
    }, headers=auth_headers)

    data = response.get_json()
    assert response.status_code == 201
    tag_names = [t["name"] for t in data["note"]["tags"]]
    assert "work" in tag_names
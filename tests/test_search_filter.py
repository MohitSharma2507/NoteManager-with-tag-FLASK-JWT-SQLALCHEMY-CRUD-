def test_search_filter(client, auth_headers):

    client.post("/api/notes/add_note",json={
        "title":"New Flask Note",
        "content":"Note Added",
        "tags":["tag1","tag2","tag3"]
    },
    headers=auth_headers
    )

    response = client.get("/api/notes/get_notes?search=Flask",
               headers=auth_headers)
    data = response.get_json()           
    assert response.status_code == 200
    assert len(data["notes"]) >= 1
    assert "Flask" in data["notes"][0]["title"]

def test_filter_by_tag(client, auth_headers):
    client.post("/api/notes/add_note", json={
        "title": "Tagged note",
        "content": "Has a tag",
        "tags": ["work","leave"]
    }, headers=auth_headers)

    response = client.get("/api/notes/get_notes?tag=work",
                          headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data["notes"]) >= 1
    all_tag_names = [
        t["name"]
        for note in data["notes"]       # loop through every note
        for t in note["tags"]           # loop through every tag in that note
         ]
    assert "leave" in all_tag_names   
    


import pytest

@pytest.mark.order(13)
def test_remove_tag(client, auth_headers):
  
    create = client.post("/api/notes/add_note",json={
        "title":"Adding note",
        "content":"Note Added sucessfully",
        "tags":["tag1","tag2","tag3"]
    },
    headers = auth_headers
    )
    note_id = create.get_json()["note"]["id"]   
    tag_response = client.get('/api/tags/get_tags', headers = auth_headers)
    tag_id = tag_response.get_json()["tags"][0]["id"]

    respone = client.post(f"/api/tags/remove_tag/{note_id}", json={
     "tag_id":tag_id
    },headers = auth_headers)

    data = respone.get_json()

    assert respone.status_code ==201
    assert "message" in data
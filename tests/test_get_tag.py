import pytest

@pytest.mark.order(11)
def test_get_tag(client, auth_headers):
  
    create = client.post("/api/tags/add_tag",json={
        "name":"New Tag"
    },
    headers = auth_headers)
    
    tag_id = create.get_json()["tag"]["id"]
    respone = client.get(f"/api/tags/get_tag/{tag_id}",headers = auth_headers)

    data = respone.get_json()

    assert respone.status_code ==200
    assert data["tag"]["id"] == tag_id

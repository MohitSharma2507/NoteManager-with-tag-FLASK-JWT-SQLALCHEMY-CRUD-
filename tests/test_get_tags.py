import pytest

@pytest.mark.order(12)
def test_get_tags(client, auth_headers):
  
   
    respone = client.get(f"/api/tags/get_tags",headers = auth_headers)

    data = respone.get_json()

    assert respone.status_code ==200
    assert "tags" in data

import pytest

@pytest.mark.order(10)
def test_add_tag(client, auth_headers):

    respone = client.post("/api/tags/add_tag",json={
        "name":"New Tag"
    },
    headers = auth_headers)

    assert respone.status_code == 201


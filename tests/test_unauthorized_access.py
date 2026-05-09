import pytest

@pytest.mark.order(8)
def test_unauthorized_access(client):

    response = client.get("/api/notes/get_notes")

    assert response.status_code == 401
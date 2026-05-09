import pytest

@pytest.mark.order(3)
def test_create_note_invalid(client, auth_headers):

    response = client.post(
        "/api/notes/add_note",
        json={"content": "Missing title"},
        headers=auth_headers
    )

    assert response.status_code == 400
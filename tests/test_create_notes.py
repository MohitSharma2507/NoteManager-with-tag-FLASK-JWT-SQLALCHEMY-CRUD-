from tests.conftest import auth_headers
import pytest


@pytest.mark.order(4)
def test_create_notes(client,auth_headers):

    response = client.post("/api/notes/add_note",json={
        "title":"Adding note",
        "content":"Note Added sucessfully",
        "tags":["tag1","tag2","tag3"]
    },
    headers = auth_headers
      )
    data = response.get_json()
    print("Response of notes created ", data)

# Message Validation
    assert data["message"] == "Note Created"

# Note Structure Validation
    note = data["note"]

    assert "id" in note
    assert "title" in note
    assert "content" in note
    assert "tags" in note
    assert "is_pinned" in note
  
#  Value Assertions
    assert note["title"] == "Adding note"
    assert note["content"] == "Note Added sucessfully"
    assert note["is_pinned"] is False 

# Tags Validation
    tags = note["tags"]

    assert isinstance(tags,list)
    assert isinstance(note["id"], int)
    assert len(tags) == 3

# 🔍 Validate each tag
    tag_names =[t["name"] for t in tags]

    assert "tag1" in tag_names
    assert "tag2" in tag_names
    assert "tag3" in tag_names







from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.matchers import IsNowUTC, IsPositiveInt
from tests.utils import create_tag

##################
##### CREATE #####
##################


def test_create_tag_success(client: TestClient) -> None:
    response = client.post("/api/tags", json={"name": "testing"})

    assert response.status_code == 201
    assert response.json() == {
        "name": "testing",
        "slug": "testing",
        "id": IsPositiveInt,
        "created_at": IsNowUTC,
    }


def test_create_tag_duplicate_tag_error(client: TestClient, db: Session) -> None:
    create_tag(db)
    response = client.post("/api/tags", json={"name": "testing"})

    assert response.status_code == 409
    assert response.json() == {"detail": "Tag already exists"}


def test_create_tag_slug_is_name_slugified(client: TestClient) -> None:
    response = client.post("/api/tags", json={"name": "My First Tag!"})
    data = response.json()

    assert response.status_code == 201
    assert data["slug"] == "my-first-tag"


##################
###### GET #######
##################


def test_get_tags_success(client: TestClient, db: Session) -> None:
    tag_one = create_tag(db)
    tag_two = create_tag(session=db, name="Philosophy")
    response = client.get("/api/tags")

    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "name": "testing",
                "slug": "testing",
                "id": tag_one.id,
                "created_at": IsNowUTC,
            },
            {
                "name": "Philosophy",
                "slug": "philosophy",
                "id": tag_two.id,
                "created_at": IsNowUTC,
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 50,
        "has_more": False,
    }


def test_get_tags_empty(client: TestClient) -> None:
    response = client.get("/api/tags")

    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0, "skip": 0, "limit": 50, "has_more": False}


def test_get_tags_pagination_success(client: TestClient, db: Session) -> None:
    create_tag(db)
    create_tag(session=db, name="Philosophy")
    create_tag(session=db, name="History")
    response = client.get("/api/tags", params={"limit": 2})
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["total"] == 3
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert data["has_more"] is True


def test_get_tags_pagination_invalid_params(client: TestClient) -> None:
    skip_response = client.get("/api/tags", params={"skip": -1})
    limit_response = client.get("/api/tags", params={"limit": 101})

    assert skip_response.status_code == 422
    assert limit_response.status_code == 422


def test_get_tag_success(client: TestClient, db: Session) -> None:
    tag = create_tag(db)
    response = client.get(f"/api/tags/{tag.id}")

    assert response.status_code == 200
    assert response.json() == {
        "name": "testing",
        "slug": "testing",
        "id": tag.id,
        "created_at": IsNowUTC,
    }


def test_get_tag_not_found(client: TestClient) -> None:
    response = client.get("/api/tags/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tag not found"}


##################
##### UPDATE #####
##################


def test_update_tag_success(client: TestClient, db: Session) -> None:
    tag = create_tag(db)
    response = client.patch(f"/api/tags/{tag.id}", json={"name": "Updated Tag"})

    assert response.status_code == 200
    assert response.json() == {
        "name": "Updated Tag",
        "slug": "updated-tag",
        "id": tag.id,
        "created_at": IsNowUTC,
    }


def test_update_tag_not_found(client: TestClient) -> None:
    response = client.patch("/api/tags/999", json={"name": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Tag not found"}


def test_update_tag_duplicate_tag_error(client: TestClient, db: Session) -> None:
    create_tag(db)
    tag_two = create_tag(session=db, name="Philosophy")
    response = client.patch(f"/api/tags/{tag_two.id}", json={"name": "testing"})

    assert response.status_code == 409
    assert response.json() == {"detail": "Tag with that name already exists"}


##################
##### DELETE #####
##################


def test_delete_tag_success(client: TestClient, db: Session) -> None:
    tag = create_tag(db)
    response = client.delete(f"/api/tags/{tag.id}")

    assert response.status_code == 204


def test_delete_tag_not_found(client: TestClient) -> None:
    response = client.delete("/api/tags/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tag not found"}

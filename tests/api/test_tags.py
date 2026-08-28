from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.matchers import IsNowUTC, IsPositiveInt
from tests.utils import create_author, create_excerpt, create_source, create_tag

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


def test_get_tag_excerpts_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    tag_one = create_tag(db)
    tag_two = create_tag(db, name="tag-two")
    excerpt_one = create_excerpt(session=db, source_id=source.id, tags=[tag_one])
    excerpt_two = create_excerpt(session=db, source_id=source.id, content="Excerpt Two", tags=[tag_one])
    _excerpt_three = create_excerpt(session=db, source_id=source.id, content="Excerpt Three", tags=[tag_two])
    response = client.get(f"/api/tags/{tag_one.id}/excerpts")

    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "content": "Test Excerpt",
                "locator": "Page 1",
                "meta": None,
                "id": excerpt_one.id,
                "created_at": IsNowUTC,
                "source": {
                    "title": source.title,
                    "cover_image_file": None,
                    "type": "book",
                    "id": source.id,
                    "created_at": IsNowUTC,
                    "author": {
                        "first_name": "Test",
                        "last_name": "Author",
                        "id": author.id,
                        "created_at": IsNowUTC,
                    },
                },
                "tags": [
                    {
                        "name": "testing",
                        "id": tag_one.id,
                        "created_at": IsNowUTC,
                        "slug": "testing",
                    }
                ],
            },
            {
                "content": "Excerpt Two",
                "locator": "Page 1",
                "meta": None,
                "id": excerpt_two.id,
                "created_at": IsNowUTC,
                "source": {
                    "title": source.title,
                    "cover_image_file": None,
                    "type": "book",
                    "id": source.id,
                    "created_at": IsNowUTC,
                    "author": {
                        "first_name": "Test",
                        "last_name": "Author",
                        "id": author.id,
                        "created_at": IsNowUTC,
                    },
                },
                "tags": [
                    {
                        "name": "testing",
                        "id": tag_one.id,
                        "created_at": IsNowUTC,
                        "slug": "testing",
                    }
                ],
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 50,
        "has_more": False,
    }


def test_get_tag_excerpts_no_excerpts(client: TestClient, db: Session) -> None:
    author = create_author(db)
    _source = create_source(session=db, author_id=author.id)
    tag = create_tag(db)
    response = client.get(f"/api/tags/{tag.id}/excerpts")

    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0, "skip": 0, "limit": 50, "has_more": False}


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


def test_update_tag_duplicate_tag_error(client: TestClient, db: Session) -> None:
    create_tag(db)
    tag_two = create_tag(session=db, name="Philosophy")
    response = client.patch(f"/api/tags/{tag_two.id}", json={"name": "testing"})

    assert response.status_code == 409
    assert response.json() == {"detail": "Tag already exists"}


##################
##### DELETE #####
##################


def test_delete_tag_success(client: TestClient, db: Session) -> None:
    tag = create_tag(db)
    response = client.delete(f"/api/tags/{tag.id}")

    assert response.status_code == 204

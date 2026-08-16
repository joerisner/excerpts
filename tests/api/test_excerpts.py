from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.matchers import IsNowUTC, IsPositiveInt
from tests.utils import create_author, create_excerpt, create_source

##################
##### CREATE #####
##################


def test_create_excerpt_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.post(
        "/api/excerpts",
        json={
            "content": "Test content.",
            "locator": "Page 42",
            "source_id": source.id,
            "meta": {
                "published_year": 1901,
            },
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "content": "Test content.",
        "locator": "Page 42",
        "meta": {"published_year": 1901},
        "id": IsPositiveInt,
        "created_at": IsNowUTC,
        "source": {
            "title": "Test Source",
            "cover_image_file": None,
            "type": "book",
            "id": source.id,
            "created_at": IsNowUTC,
            "author": {
                "id": author.id,
                "first_name": "Test",
                "last_name": "Author",
                "created_at": IsNowUTC,
            },
        },
    }


def test_create_excerpt_meta_defaults_to_null(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.post("/api/excerpts", json={"content": "Test excerpt.", "source_id": source.id})

    assert response.status_code == 201
    assert response.json()["meta"] is None


def test_create_excerpt_content_cannot_be_empty(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.post("/api/excerpts", json={"content": "", "source_id": source.id})

    assert response.status_code == 422


def test_create_excerpt_source_not_found_error(client: TestClient) -> None:
    response = client.post("/api/excerpts", json={"content": "Test content.", "source_id": 999})

    assert response.status_code == 422
    assert response.json() == {"detail": "Could not find source with id 999"}


##################
####### GET ######
##################


def test_get_excerpts_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt_one = create_excerpt(session=db, source_id=source.id)
    excerpt_two = create_excerpt(session=db, source_id=source.id, content="Second excerpt.", locator="Page 2")
    response = client.get("/api/excerpts")
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data == {
        "data": [
            {
                "content": "Test Excerpt",
                "locator": "Page 1",
                "meta": None,
                "id": excerpt_one.id,
                "created_at": IsNowUTC,
                "source": {
                    "title": "Test Source",
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
            },
            {
                "content": "Second excerpt.",
                "locator": "Page 2",
                "meta": None,
                "id": excerpt_two.id,
                "created_at": IsNowUTC,
                "source": {
                    "title": "Test Source",
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
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 50,
        "has_more": False,
    }


def test_get_excerpts_empty(client: TestClient) -> None:
    response = client.get("/api/excerpts")

    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0, "skip": 0, "limit": 50, "has_more": False}


def test_get_excerpts_pagination_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    create_excerpt(session=db, source_id=source.id)
    create_excerpt(session=db, source_id=source.id, content="Excerpt Two")
    create_excerpt(session=db, source_id=source.id, content="Excerpt Three")
    response = client.get("/api/excerpts", params={"limit": 2})
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["total"] == 3
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert data["has_more"] is True


def test_get_excerpts_pagination_invalid_params(client: TestClient) -> None:
    skip_response = client.get("/api/excerpts", params={"skip": -1})
    limit_response = client.get("/api/excerpts", params={"limit": 101})

    assert skip_response.status_code == 422
    assert limit_response.status_code == 422


def test_get_excerpt_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.get(f"/api/excerpts/{excerpt.id}")

    assert response.status_code == 200
    assert response.json() == {
        "content": "Test Excerpt",
        "locator": "Page 1",
        "meta": None,
        "id": excerpt.id,
        "created_at": IsNowUTC,
        "source": {
            "title": "Test Source",
            "cover_image_file": None,
            "type": "book",
            "id": source.id,
            "created_at": IsNowUTC,
            "author": {
                "id": author.id,
                "first_name": "Test",
                "last_name": "Author",
                "created_at": IsNowUTC,
            },
        },
    }


def test_get_excerpt_not_found(client: TestClient) -> None:
    response = client.get("/api/excerpts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Excerpt not found"}


##################
##### UPDATE #####
##################


def test_update_excerpt_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"content": "Updated content", "locator": "Page 99"})

    assert response.status_code == 200
    assert response.json() == {
        "content": "Updated content",
        "locator": "Page 99",
        "meta": None,
        "id": excerpt.id,
        "created_at": IsNowUTC,
        "source": {
            "title": "Test Source",
            "cover_image_file": None,
            "type": "book",
            "id": source.id,
            "created_at": IsNowUTC,
            "author": {
                "id": author.id,
                "first_name": "Test",
                "last_name": "Author",
                "created_at": IsNowUTC,
            },
        },
    }


def test_update_excerpt_not_found(client: TestClient) -> None:
    response = client.patch("/api/excerpts/999", json={"content": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Excerpt not found"}


def test_update_excerpt_to_have_different_source(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source_one = create_source(session=db, author_id=author.id)
    source_two = create_source(session=db, author_id=author.id, title="Source Two")
    excerpt = create_excerpt(session=db, source_id=source_one.id)
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"source_id": source_two.id})
    data = response.json()

    assert response.status_code == 200
    assert data["source"]["id"] == source_two.id
    assert data["source"]["title"] == "Source Two"


def test_update_excerpt_can_clear_locator_and_meta(client: TestClient, db: Session) -> None:
    """The nullable locator and meta fields can be cleared by passing null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id, locator="Page 1", meta={"tags": ["x"]})
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"locator": None, "meta": None})
    data = response.json()

    assert response.status_code == 200
    assert data["locator"] is None
    assert data["meta"] is None


def test_update_excerpt_content_cannot_be_null(client: TestClient, db: Session) -> None:
    """When included in the request, the content field cannot be null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"content": None})

    assert response.status_code == 422
    assert "content cannot be null" in response.text


def test_update_excerpt_source_id_cannot_be_null(client: TestClient, db: Session) -> None:
    """When included in the request, the source_id field cannot be null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"source_id": None})

    assert response.status_code == 422
    assert "source_id cannot be null" in response.text


def test_update_excerpt_source_not_found_error(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.patch(f"/api/excerpts/{excerpt.id}", json={"source_id": 999})

    assert response.status_code == 422
    assert response.json() == {"detail": "Could not find source with id 999"}


##################
##### DELETE #####
##################


def test_delete_excerpt_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    response = client.delete(f"/api/excerpts/{excerpt.id}")

    assert response.status_code == 204


def test_delete_excerpt_not_found(client: TestClient) -> None:
    response = client.delete("/api/excerpts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Excerpt not found"}

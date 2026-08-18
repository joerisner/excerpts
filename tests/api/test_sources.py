from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.matchers import IsNowUTC, IsPositiveInt
from tests.utils import create_author, create_excerpt, create_source

##################
##### CREATE #####
##################


def test_create_source_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.post(
        "/api/sources",
        json={"title": "Test Source", "cover_image_file": None, "type": "article", "author_id": author.id},
    )

    assert response.status_code == 201
    assert response.json() == {
        "title": "Test Source",
        "cover_image_file": None,
        "type": "article",
        "id": IsPositiveInt,
        "created_at": IsNowUTC,
        "author": {
            "id": author.id,
            "first_name": "Test",
            "last_name": "Author",
            "created_at": IsNowUTC,
        },
    }


def test_create_source_duplicate_source_error(client: TestClient, db: Session) -> None:
    author = create_author(db)
    existing_source = create_source(session=db, author_id=author.id)
    response = client.post("/api/sources", json={"title": existing_source.title, "author_id": author.id})

    assert response.status_code == 409
    assert response.json() == {"detail": "Source by that title and author already exists"}


def test_create_source_same_title_allowed_for_different_authors(client: TestClient, db: Session) -> None:
    author_one = create_author(db)
    author_two = create_author(session=db, last_name="AuthorTwo")
    existing_source = create_source(session=db, author_id=author_one.id)
    response = client.post("/api/sources", json={"title": existing_source.title, "author_id": author_two.id})

    assert response.status_code == 201


def test_create_source_source_type_must_be_enum_value(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.post("/api/sources", json={"title": "Test Source", "author_id": author.id, "type": "journal"})

    assert response.status_code == 422


##################
####### GET ######
##################


def test_get_sources_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source_one = create_source(session=db, author_id=author.id)
    source_two = create_source(session=db, author_id=author.id, title="Source Two", type="video")
    response = client.get("/api/sources")
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data == {
        "data": [
            {
                "title": "Test Source",
                "cover_image_file": None,
                "type": "book",
                "id": source_one.id,
                "created_at": IsNowUTC,
                "author": {
                    "first_name": "Test",
                    "last_name": "Author",
                    "id": author.id,
                    "created_at": IsNowUTC,
                },
            },
            {
                "title": "Source Two",
                "cover_image_file": None,
                "type": "video",
                "id": source_two.id,
                "created_at": IsNowUTC,
                "author": {
                    "first_name": "Test",
                    "last_name": "Author",
                    "id": author.id,
                    "created_at": IsNowUTC,
                },
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 20,
        "has_more": False,
    }


def test_get_sources_empty(client: TestClient) -> None:
    response = client.get("/api/sources")
    data = response.json()

    assert response.status_code == 200
    assert data == {"data": [], "total": 0, "skip": 0, "limit": 20, "has_more": False}


def test_get_sources_pagination_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    create_source(session=db, author_id=author.id)
    create_source(session=db, author_id=author.id, title="Source Two")
    create_source(session=db, author_id=author.id, title="Source Three")
    response = client.get("/api/sources", params={"limit": 2})
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["total"] == 3
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert data["has_more"] is True


def test_get_sources_pagination_invalid_params(client: TestClient) -> None:
    skip_response = client.get("/api/sources", params={"skip": -1})
    limit_response = client.get("/api/sources", params={"limit": 101})

    assert skip_response.status_code == 422
    assert limit_response.status_code == 422


def test_get_source_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.get(f"/api/sources/{source.id}")

    assert response.status_code == 200
    assert response.json() == {
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
    }


def test_get_source_not_found(client: TestClient) -> None:
    response = client.get("/api/sources/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}


def test_get_source_excerpts_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt_one = create_excerpt(session=db, source_id=source.id)
    excerpt_two = create_excerpt(session=db, source_id=source.id, content="Excerpt Two")
    response = client.get(f"/api/sources/{source.id}/excerpts")

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
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 50,
        "has_more": False,
    }


def test_get_source_excerpts_source_not_found(client: TestClient) -> None:
    response = client.get("/api/sources/999/excerpts")

    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}


def test_get_source_excerpts_no_excerpts(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.get(f"/api/sources/{source.id}/excerpts")

    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0, "skip": 0, "limit": 50, "has_more": False}


##################
##### UPDATE #####
##################


def test_update_source_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.patch(f"/api/sources/{source.id}", json={"title": "Updated Title", "type": "podcast"})

    assert response.status_code == 200
    assert response.json() == {
        "title": "Updated Title",
        "cover_image_file": None,
        "type": "podcast",
        "id": source.id,
        "created_at": IsNowUTC,
        "author": {
            "id": author.id,
            "first_name": "Test",
            "last_name": "Author",
            "created_at": IsNowUTC,
        },
    }


def test_update_source_not_found(client: TestClient) -> None:
    response = client.patch("/api/sources/999", json={"title": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}


def test_update_source_to_have_different_author(client: TestClient, db: Session) -> None:
    author_one = create_author(db)
    author_two = create_author(session=db, last_name="AuthorTwo")
    source = create_source(session=db, author_id=author_one.id)
    response = client.patch(f"/api/sources/{source.id}", json={"author_id": author_two.id})
    data = response.json()

    assert response.status_code == 200
    assert data["author"]["id"] == author_two.id
    assert data["author"]["last_name"] == "AuthorTwo"


def test_update_source_duplicate_source_error_same_author(client: TestClient, db: Session) -> None:
    author_one = create_author(db)
    source_one = create_source(session=db, author_id=author_one.id, title="Source One")
    source_two = create_source(session=db, author_id=author_one.id, title="Source Two")
    response = client.patch(f"/api/sources/{source_two.id}", json={"title": source_one.title})

    assert response.status_code == 409
    assert response.json() == {"detail": "Source by that title and author already exists"}


def test_update_source_duplicate_source_error_different_author(client: TestClient, db: Session) -> None:
    author_one = create_author(db)
    author_two = create_author(session=db, last_name="AuthorTwo")
    _author_one_source = create_source(session=db, author_id=author_one.id, title="Same")
    author_two_source = create_source(session=db, author_id=author_two.id, title="Same")
    response = client.patch(f"/api/sources/{author_two_source.id}", json={"author_id": author_one.id})

    assert response.status_code == 409
    assert response.json() == {"detail": "Source by that title and author already exists"}


def test_update_source_title_cannot_be_null(client: TestClient, db: Session) -> None:
    """When included in the request, the title field cannot be null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.patch(f"/api/sources/{source.id}", json={"title": None})

    assert response.status_code == 422
    assert "title cannot be null" in response.text


def test_update_source_type_cannot_be_null(client: TestClient, db: Session) -> None:
    """When included in the request, the type field cannot be null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.patch(f"/api/sources/{source.id}", json={"type": None})

    assert response.status_code == 422
    assert "type cannot be null" in response.text


def test_update_source_author_id_cannot_be_null(client: TestClient, db: Session) -> None:
    """When included in the request, the author_id field cannot be null."""
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.patch(f"/api/sources/{source.id}", json={"author_id": None})

    assert response.status_code == 422
    assert "author_id cannot be null" in response.text


##################
##### DELETE #####
##################


def test_delete_source_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    response = client.delete(f"/api/sources/{source.id}")

    assert response.status_code == 204


def test_delete_source_not_found(client: TestClient) -> None:
    response = client.delete("/api/sources/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}

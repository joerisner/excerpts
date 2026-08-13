from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.matchers import IsNowUTC, IsPositiveInt
from tests.utils import create_author

##################
##### CREATE #####
##################


def test_create_author_success(client: TestClient) -> None:
    response = client.post("/api/authors", json={"first_name": "Nick", "last_name": "Miller"})

    assert response.status_code == 201
    assert response.json() == {
        "id": IsPositiveInt,
        "first_name": "Nick",
        "last_name": "Miller",
        "created_at": IsNowUTC,
    }


def test_create_mononym_author_success(client: TestClient) -> None:
    response = client.post("/api/authors", json={"last_name": "Homer"})
    data = response.json()

    assert response.status_code == 201
    assert data["first_name"] is None
    assert data["last_name"] == "Homer"


def test_create_duplicate_author_error(client: TestClient, db: Session) -> None:
    create_author(db)
    response = client.post("/api/authors", json={"first_name": "Test", "last_name": "AuThOr"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Author already exists with that name"}


##################
####### GET ######
##################


def test_get_authors_success(client: TestClient, db: Session) -> None:
    author_one = create_author(db)
    author_two = create_author(session=db, first_name="Nick", last_name="Miller")
    response = client.get("/api/authors")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "data": [
            {
                "id": author_one.id,
                "first_name": "Test",
                "last_name": "Author",
                "created_at": IsNowUTC,
            },
            {
                "id": author_two.id,
                "first_name": "Nick",
                "last_name": "Miller",
                "created_at": IsNowUTC,
            },
        ],
        "total": 2,
        "skip": 0,
        "limit": 20,
        "has_more": False,
    }


def test_get_authors_empty(client: TestClient) -> None:
    response = client.get("/api/authors")
    data = response.json()

    assert response.status_code == 200
    assert data == {"data": [], "total": 0, "skip": 0, "limit": 20, "has_more": False}


def test_get_authors_pagination_success(client: TestClient, db: Session) -> None:
    create_author(db)
    create_author(db, first_name="Author", last_name="Two")
    create_author(db, last_name="Three")
    response = client.get("/api/authors", params={"limit": 2})
    data = response.json()

    assert response.status_code == 200
    assert len(data["data"]) == 2
    assert data["total"] == 3
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert data["has_more"] is True


def test_get_authors_pagination_invalid_params(client: TestClient) -> None:
    skip_response = client.get("/api/authors", params={"skip": -1})
    limit_response = client.get("/api/authors", params={"limit": 101})

    assert skip_response.status_code == 422
    assert limit_response.status_code == 422


def test_get_author_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.get(f"/api/authors/{author.id}")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "id": author.id,
        "first_name": "Test",
        "last_name": "Author",
        "created_at": IsNowUTC,
    }


def test_get_author_not_found(client: TestClient) -> None:
    response = client.get("/api/authors/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


##################
##### UPDATE #####
##################


def test_update_author_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.patch(f"/api/authors/{author.id}", json={"last_name": "Updated"})

    assert response.status_code == 200
    assert response.json() == {
        "id": author.id,
        "first_name": "Test",
        "last_name": "Updated",
        "created_at": IsNowUTC,
    }


def test_update_author_not_found(client: TestClient) -> None:
    response = client.patch("/api/authors/999", json={"first_name": "Missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


def test_update_author_cannot_include_null_last_name(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.patch(f"/api/authors/{author.id}", json={"last_name": None})

    assert response.status_code == 422
    assert "last name cannot be null" in response.text


def test_update_duplicate_author_error(client: TestClient, db: Session) -> None:
    create_author(db)
    author_two = create_author(db, first_name="Test", last_name="AuthorTwo")
    response = client.patch(f"/api/authors/{author_two.id}", json={"last_name": "AuThOr"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Author already exists with that name"}


##################
##### DELETE #####
##################


def test_delete_author_success(client: TestClient, db: Session) -> None:
    author = create_author(db)
    response = client.delete(f"/api/authors/{author.id}")

    assert response.status_code == 204


def test_delete_author_not_found(client: TestClient) -> None:
    response = client.delete("/api/authors/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}

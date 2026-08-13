from sqlalchemy.orm import Session

from excerpts.models.author import Author
from tests.matchers import IsNowUTC


def test_create_mononym_author_success(db: Session) -> None:
    author = Author(last_name="Homer")
    db.add(author)
    db.commit()
    data = db.get_one(Author, author.id, populate_existing=False)

    assert data.first_name is None
    assert data.created_at == IsNowUTC

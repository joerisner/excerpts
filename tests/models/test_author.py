from datetime import UTC, datetime

from dirty_equals import IsDatetime
from sqlalchemy.orm import Session

from excerpts.models.author import Author


def test_create_mononym_author_success(db: Session) -> None:
    author = Author(last_name="Homer")

    db.add(author)
    db.commit()

    result = db.get_one(Author, author.id, populate_existing=False)
    assert result.first_name is None
    assert result.created_at == IsDatetime(approx=datetime.now(UTC), delta=5)

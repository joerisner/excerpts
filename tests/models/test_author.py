from dirty_equals._datetime import IsDatetime
from dirty_equals._numeric import IsPositiveInt
from sqlalchemy.orm import Session

from excerpts.models.author import Author


def test_create_mononym_author_success(db: Session):
    author = Author(last_name="Homer")

    db.add(author)
    db.commit()

    assert author.id == IsPositiveInt()
    assert author.first_name is None
    assert author.last_name == "Homer"
    assert author.created_at == IsDatetime(iso_string=True)

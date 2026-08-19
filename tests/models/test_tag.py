import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from excerpts.models.tag import Tag


def test_tag_slug_must_be_lowercase(db: Session) -> None:
    tag = Tag(name="Education", slug="Education")
    db.add(tag)

    with pytest.raises(IntegrityError):
        db.commit()


def test_tag_slug_must_be_unique(db: Session) -> None:
    tag_one = Tag(name="Education", slug="education")
    db.add(tag_one)
    db.commit()

    tag_two = Tag(name="education", slug="education")
    db.add(tag_two)

    with pytest.raises(IntegrityError):
        db.commit()

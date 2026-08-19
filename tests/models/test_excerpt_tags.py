import warnings

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from excerpts.models.excerpt_tag import ExcerptTag
from tests.utils import create_author, create_excerpt, create_source, create_tag


def test_excerpt_tag_row_must_be_unique(db: Session) -> None:
    author = create_author(db)
    source = create_source(session=db, author_id=author.id)
    excerpt = create_excerpt(session=db, source_id=source.id)
    tag = create_tag(db)
    excerpt_tag_one = ExcerptTag(excerpt_id=excerpt.id, tag_id=tag.id)
    db.add(excerpt_tag_one)
    db.commit()
    excerpt_tag_two = ExcerptTag(excerpt_id=excerpt.id, tag_id=tag.id)
    db.add(excerpt_tag_two)

    with warnings.catch_warnings(record=True), pytest.raises(IntegrityError):
        db.commit()

import pytest
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from excerpts.models.source import Source
from tests.utils import create_test_author


def test_cover_image_path_uses_default_cover_image(db: Session) -> None:
    author = create_test_author(db)
    source = Source(title="My Podcast", type="podcast", author=author)

    db.add(source)
    db.commit()

    result = db.get_one(Source, source.id, populate_existing=False)
    assert result.cover_image_file is None
    assert result.cover_image_path.endswith("/images/default_cover_image.png")


# TODO: This is temporary until S3 is implemented.
def test_cover_image_path_raises_error(db: Session) -> None:
    author = create_test_author(db)
    source = Source(title="My Source with Image", type="essay", cover_image_file="foo.png", author=author)

    db.add(source)
    db.commit()

    result = db.get_one(Source, source.id, populate_existing=False)

    with pytest.raises(NotImplementedError, match="S3 cover image resolution not yet implemented"):
        result.cover_image_path


def test_source_type_must_be_enum_value(db: Session) -> None:
    author = create_test_author(db)
    source = Source(title="My Essay", type="ESSAY", author=author)

    db.add(source)

    with pytest.raises(DataError):
        db.commit()

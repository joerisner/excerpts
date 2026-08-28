import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from excerpts.api.utils import get_or_404, resolve_tags
from excerpts.models.author import Author
from excerpts.models.tag import Tag
from tests.utils import create_author, create_tag


def test_get_or_404_returns_resource_when_found(db: Session) -> None:
    author = create_author(db)
    result = get_or_404(db=db, model=Author, id=author.id)

    assert isinstance(result, Author)
    assert result.id == author.id


def test_get_or_404_responds_with_404_when_resource_not_found(db: Session) -> None:
    with pytest.raises(HTTPException, match="404: Author not found"):
        get_or_404(db=db, model=Author, id=999)


def test_resolve_tags_returns_list_of_tags(db: Session) -> None:
    tag_one = create_tag(session=db, name="education")
    tag_two = create_tag(session=db, name="Philosophy")
    tags = resolve_tags(db=db, names=["Education", "Philosophy"])

    assert tags == [tag_one, tag_two]


def test_resolve_tags_creates_tag_when_not_found(db: Session) -> None:
    create_tag(session=db, name="education")
    tags = resolve_tags(db=db, names=["education", "philosophy", "inspiration"])

    assert len(tags) == 3
    assert all(isinstance(tag, Tag) for tag in tags)


def test_resolve_tags_does_not_duplicate_tags(db: Session) -> None:
    create_tag(session=db, name="education")
    tags = resolve_tags(db=db, names=["education", "Education"])

    assert len(tags) == 1
    assert isinstance(tags[0], Tag)

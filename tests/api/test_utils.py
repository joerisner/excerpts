import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from excerpts.api.utils import get_or_404
from excerpts.models.author import Author
from tests.utils import create_author


def test_get_or_404_returns_resource_when_found(db: Session) -> None:
    author = create_author(db)
    result = get_or_404(db=db, model=Author, id=author.id)

    assert isinstance(result, Author)
    assert result.id == author.id


def test_get_or_404_responds_with_404_when_resource_not_found(db: Session) -> None:
    with pytest.raises(HTTPException, match="404: Author not found"):
        get_or_404(db=db, model=Author, id=999)

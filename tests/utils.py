from typing import Any

from sqlalchemy.orm import Session

from excerpts.models.author import Author
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source
from excerpts.models.tag import Tag
from excerpts.utils.string import slugify


def create_author(session: Session, first_name: str | None = "Test", last_name: str = "Author") -> Author:
    """
    Create an author using the ORM directly.
    Returns:
      - Author
    """
    author = Author(first_name=first_name, last_name=last_name)

    session.add(author)
    session.commit()
    session.refresh(author)
    return author


def create_source(
    session: Session,
    author_id: int,
    title: str = "Test Source",
    cover_image_file: str | None = None,
    type: str = "book",
) -> Source:
    """
    Create a source using the ORM directly.
    Returns:
      - Source
    """
    source = Source(title=title, cover_image_file=cover_image_file, type=type, author_id=author_id)

    session.add(source)
    session.commit()
    session.refresh(source)
    return source


def create_excerpt(
    session: Session,
    source_id: int,
    content: str | None = "Test Excerpt",
    locator: str | None = "Page 1",
    meta: dict[str, Any] | None = None,
    tags: list[Tag] | None = None,
) -> Excerpt:
    """
    Create an excerpt using the ORM directly.
    Returns:
      - Excerpt
    """
    excerpt = Excerpt(source_id=source_id, content=content, locator=locator, meta=meta)

    if tags:
        excerpt.tags = tags

    session.add(excerpt)
    session.commit()
    session.refresh(excerpt)
    return excerpt


def create_tag(session: Session, name: str = "testing") -> Tag:
    """
    Create a tag using the ORM directly.
    Returns:
      - Tag
    """
    tag = Tag(name=name, slug=slugify(name))

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

from sqlalchemy.orm import Session

from excerpts.models.author import Author
from excerpts.models.source import Source


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

from sqlalchemy.orm import Session

from excerpts.models.author import Author


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

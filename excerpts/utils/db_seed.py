"""
Seed the local development database.
This script should only ever run in the `dev` environment.
"""

from excerpts.core.config import config
from excerpts.core.db import SessionLocal
from excerpts.models.author import Author
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source


def seed_authors() -> None:
    with SessionLocal() as session:
        author = Author(first_name="John", last_name="Bunyan")
        session.add(author)
        session.commit()


def seed_sources() -> None:
    with SessionLocal() as session:
        source = Source(title="The Pilgrim's Progress", type="book", author=session.get(Author, 1))
        session.add(source)
        session.commit()


def seed_excerpts() -> None:
    with SessionLocal() as session:
        excerpt = Excerpt(
            content="There is therefore knowledge and knowledge.",
            locator="Page 86",
            source=session.get(Source, 1),
        )
        session.add(excerpt)
        session.commit()


def main() -> None:
    seed_authors()
    seed_sources()
    seed_excerpts()


if __name__ == "__main__":
    if config.ENVIRONMENT != "dev":
        raise RuntimeError("Seed script should only run in dev environment")
    main()

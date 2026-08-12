"""
Truncate all tables in the local development database, clearing out all data.
This script should only ever run in the `dev` environment.
"""

from sqlalchemy import delete, text

from excerpts.core.config import config
from excerpts.core.db import SessionLocal
from excerpts.models.author import Author
from excerpts.models.excerpt import Excerpt
from excerpts.models.source import Source

# NOTE: Order matters.
models = [Excerpt, Source, Author]


def main() -> None:
    with SessionLocal() as session:
        for model in models:
            # Delete records.
            stmt = delete(model)
            session.execute(stmt)

            # Restart PK sequence at 1.
            tablename = model.__tablename__
            stmt = text(f"ALTER SEQUENCE {tablename}_id_seq RESTART WITH 1;")
            session.execute(statement=stmt)
            session.commit()


if __name__ == "__main__":
    if config.ENVIRONMENT != "dev":
        raise RuntimeError("Reset script should only run in dev environment")
    main()

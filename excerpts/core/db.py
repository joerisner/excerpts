from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from excerpts.core.config import config

engine = create_engine(url=config.DATABASE_URL, echo=config.ECHO_SQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    with SessionLocal() as session:
        yield session

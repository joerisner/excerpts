from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, NullPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from excerpts.core.config import config
from excerpts.main import app
from excerpts.models.base import Base


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine]:
    """
    Creates an engine, scoped to the entire test session.
    Creates the db schema and after the tests finish, drops it.
    """
    engine = create_engine(url=config.DATABASE_URL, poolclass=NullPool)
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
    yield engine
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)
    engine.dispose()


@pytest.fixture
def db(test_engine) -> Generator[Session]:
    """
    Provides a session, scoped to a single test.
    Opens a transaction and after the test finishes, rolls it back.
    """
    conn = test_engine.connect()
    trans = conn.begin()

    test_session = sessionmaker(
        bind=conn,
        class_=Session,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    with test_session() as session:
        try:
            yield session
        finally:
            trans.rollback()
            conn.close()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    """
    Provides a test client for API tests, scoped to the module.
    """
    with TestClient(app=app, base_url="http://test") as c:
        yield c

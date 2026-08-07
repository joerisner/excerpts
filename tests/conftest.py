from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from excerpts.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app=app, base_url="http://test") as c:
        yield c

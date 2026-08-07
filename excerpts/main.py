from fastapi import FastAPI

from excerpts.api.main import api_router
from excerpts.core.config import config

app = FastAPI(
    title=config.PROJECT_NAME,
    openapi_url=config.API_OPENAPI_URL,
    docs_url=config.API_DOCS_URL,
    redoc_url=None,
)

app.include_router(api_router, prefix=config.API_PREFIX)

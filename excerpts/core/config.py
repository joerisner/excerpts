from typing import Literal, Self

from pydantic import PostgresDsn, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Excerpts"
    ENVIRONMENT: Literal["dev", "test", "prod"]

    # API
    API_PREFIX: str = "/api"
    API_OPENAPI_URL: str | None = None
    API_DOCS_URL: str | None = "/api/docs"
    API_STATIC_ASSETS_DIR: str = "/excerpts/assets"

    # Database
    ECHO_SQL: bool = False
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"  # noqa: S105
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def POSTGRES_DB(self) -> str:  # noqa: N802
        return self.ENVIRONMENT

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:  # noqa: N802
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        if self.POSTGRES_PASSWORD == "password" and self.ENVIRONMENT not in ["dev", "test"]:  # noqa: S105
            raise ValueError("Refusing to use default value for POSTGRES_PASSWORD.")

        return self


config = Config()  # pyright: ignore[reportCallIssue] - Values loaded from ENV.

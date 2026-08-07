from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Excerpts"

    API_PREFIX: str = "/api"
    API_OPENAPI_URL: str | None = None
    API_DOCS_URL: str | None = "/api/docs"


config = Config()

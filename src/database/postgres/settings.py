from functools import cache

from pydantic import Field
from sqlalchemy import URL

from src.settings import BaseProjectSettings


class DatabaseSettings(BaseProjectSettings):
    """PostgreSQL connection settings sourced from environment variables."""

    pg_host: str = Field(alias="PG_HOST")
    pg_port: int = Field(alias="PG_PORT")
    pg_user: str = Field(alias="PG_USER")
    pg_name: str = Field(alias="PG_NAME")
    pg_pass: str = Field(alias="PG_PASS")

    @property
    def url(self) -> str:
        """SQLAlchemy connection URL.

        Built via URL.create so special characters in the password are
        properly URL-encoded. hide_password=False emits the real password
        — never log this value as-is.
        """
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.pg_host,
            port=self.pg_port,
            username=self.pg_user,
            password=self.pg_pass,
            database=self.pg_name,
        ).render_as_string(hide_password=False)


# noinspection PyArgumentList
@cache
def get_database_settings() -> DatabaseSettings:
    """Return the singleton DatabaseSettings instance.

    pydantic-settings parses env vars on instantiation; @cache makes this
    a process-wide singleton so env is read only once.
    """
    return DatabaseSettings()  # pyright: ignore[reportCallIssue]
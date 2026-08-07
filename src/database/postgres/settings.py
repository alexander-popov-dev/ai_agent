from functools import cache

from pydantic import Field
from sqlalchemy import URL

from src.settings import BaseProjectSettings


class DatabaseSettings(BaseProjectSettings):
    """PostgreSQL connection settings sourced from environment variables."""

    db_host: str = Field(alias="DB_HOST")
    db_user: str = Field(alias="DB_USER")
    db_name: str = Field(alias="DB_NAME")
    db_pass: str = Field(alias="DB_PASS")

    @property
    def url(self) -> str:
        """SQLAlchemy connection URL.

        Built via URL.create so special characters in the password are
        properly URL-encoded. hide_password=False emits the real password
        — never log this value as-is.
        """
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.db_host,
            username=self.db_user,
            password=self.db_pass,
            database=self.db_name,
        ).render_as_string(hide_password=False)


# noinspection PyArgumentList
@cache
def get_database_settings() -> DatabaseSettings:
    """Return the singleton DatabaseSettings instance.

    pydantic-settings parses env vars on instantiation; @cache makes this
    a process-wide singleton so env is read only once.
    """
    return DatabaseSettings()  # pyright: ignore[reportCallIssue]
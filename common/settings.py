from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from common import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PYTHON_ENV: Literal["development", "production"] = "production"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    BOT_PREFIX: str = "!"
    DEFAULT_TZ: ZoneInfo = ZoneInfo("Asia/Seoul")

    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_API_USER_AGENT: str = (
        f"kvdstudio:hannibot:v{__version__} (by /u/arockentothemoon)"
    )

    DISCORD_ADMIN_ID: int
    DISCORD_TEST_GUILD_ID: int
    DISCORD_TOKEN: str
    DISCORD_MESSAGE_PURGE_LIMIT: int = 10

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str | None = None
    POSTGRESQL_DATABASE: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int = 5432

    @property
    def IN_PRODUCTION(self) -> bool:
        return self.PYTHON_ENV == "production"

    @property
    def DATABASE_URL_PARAMS(self) -> dict[str, str | int]:
        return {
            "username": self.POSTGRESQL_USERNAME,
            "password": self.POSTGRESQL_PASSWORD,
            "host": self.POSTGRESQL_HOST,
            "port": self.POSTGRESQL_PORT,
            "path": self.POSTGRESQL_DATABASE,
        }

    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                **self.DATABASE_URL_PARAMS,
            )
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                **self.DATABASE_URL_PARAMS,
            )
        )


settings = Settings()

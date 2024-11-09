from zoneinfo import ZoneInfo

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from autocomeback import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_API_USER_AGENT: str = (
        f"cloudfunctions:autocomeback:v{__version__} (by /u/arockentothemoon)"
    )
    DEFAULT_TZ: ZoneInfo = ZoneInfo("Asia/Seoul")

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int = 5432

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

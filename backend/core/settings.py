from datetime import timedelta
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig(BaseSettings):
    env_file: str = ".env"
    model_config = SettingsConfigDict(env_file=BASE_DIR / env_file, extra="ignore")


class DatabaseSettings(BaseConfig):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    driver: str = "asyncpg"

    pg_host: str = Field(alias="PG_HOST")
    pg_password: str = Field(alias="PG_PASSWORD")
    pg_user: str = Field(alias="PG_USER")
    pg_db: str = Field(alias="PG_DB")
    pg_port: int = Field(alias="PG_PORT")

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def db_url(self) -> str:
        from sqlalchemy.engine.url import URL

        uri = URL.create(
            drivername=f"postgresql+{self.driver}",
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_db,
        )
        return uri.render_as_string(hide_password=False)


class JWTSettings(BaseConfig):
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_lifetime: timedelta = timedelta(minutes=30)
    refresh_token_lifetime: timedelta = timedelta(days=1)
    token_algorithm: str = "HS256"


class PaginationSettings(BaseConfig):
    limit: int = 10
    max_limit: int = 100


class Settings:
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    pagination: PaginationSettings = PaginationSettings()


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# If the password contains '@' symbol, we need to create the DB urls via URL.create,
# otherwise the part of the password after '@' will be considered the DB hostname

# We need to create a database with the name specified in DB_NAME in advance


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return URL.create(
            "postgresql+asyncpg",
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    @property
    def DATABASE_URL_psycopg(self):
        return URL.create(
            "postgresql+psycopg",
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

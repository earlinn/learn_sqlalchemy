from pydantic_settings import BaseSettings, SettingsConfigDict

# If the password contains '@' symbol, we need to create the DB urls via URL.create,
# otherwise the part of the password after '@' will be considered the DB hostname

# Finally I changed the postgres user password to not contain @, otherwise there
# would be errors when creating migrations via alembic

# We need to create a database with the name specified in DB_NAME in advance


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_psycopg(self):
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

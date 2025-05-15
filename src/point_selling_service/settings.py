from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings"]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    connection_string: str


class Settings(BaseSettings):
    documentation_enabled: bool = False
    database: DatabaseSettings = DatabaseSettings()

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    database_url: str
    external_api_url: str = 'https://api.randomdatatools.ru/'
    initial_load_count: int = Field(default=1000, ge=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()

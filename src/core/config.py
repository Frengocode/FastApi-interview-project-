from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///./db.sqlite3'
    db_echo: bool = True

settings = Settings()

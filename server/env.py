from dotenv import dotenv_values
from typing import TypedDict, cast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(TypedDict):
    DB_STRING: str


app_config = cast(AppConfig, dotenv_values(PROJECT_ROOT / ".env"))

from pathlib import Path
from typing import TypedDict, cast

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(TypedDict):
    DB_STRING: str
    SECRET: str


app_config = cast(AppConfig, dotenv_values(PROJECT_ROOT / ".env"))

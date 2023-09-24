from pathlib import Path
from typing import TypedDict, cast

from dotenv import dotenv_values
from litestar.middleware.session.client_side import CookieBackendConfig
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.config.compression import CompressionConfig


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(TypedDict):
    DB_STRING: str
    SECRET: str


app_config = cast(AppConfig, dotenv_values(PROJECT_ROOT / ".env"))

session_config = CookieBackendConfig(
    secret=bytes.fromhex(app_config["SECRET"]),
)

db_session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=app_config["DB_STRING"], session_config=db_session_config
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

template_config = TemplateConfig(
    directory=PROJECT_ROOT / "server/templates", engine=JinjaTemplateEngine
)
compression_config = CompressionConfig(backend="gzip")

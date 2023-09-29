from pathlib import Path
from typing import TypedDict, cast

from dotenv import dotenv_values
from litestar.middleware.session.client_side import CookieBackendConfig
from advanced_alchemy.extensions.litestar.plugins import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from advanced_alchemy.config import AsyncSessionConfig
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from litestar.config.compression import CompressionConfig


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(TypedDict):
    DB_STRING: str
    SECRET: str


app_config = cast(AppConfig, dotenv_values(PROJECT_ROOT / ".env"))

session_config = CookieBackendConfig(
    secret=bytes.fromhex(app_config["SECRET"]),
)

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=app_config["DB_STRING"],
    session_config=AsyncSessionConfig(expire_on_commit=False),
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

jinja_env = Environment(
    loader=FileSystemLoader(PROJECT_ROOT / "server/templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)

template_config = TemplateConfig(
    directory=PROJECT_ROOT / "server/templates",
    engine=JinjaTemplateEngine.from_environment(jinja_env),
)
compression_config = CompressionConfig(backend="gzip")

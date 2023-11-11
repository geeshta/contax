from pathlib import Path
from typing import TypedDict, cast

from advanced_alchemy.config import AsyncSessionConfig
from advanced_alchemy.extensions.litestar.plugins import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from dotenv import dotenv_values
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from litestar.config.compression import CompressionConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.middleware.session.client_side import CookieBackendConfig
from litestar.template.config import TemplateConfig
from litestar.config.cors import CORSConfig
from litestar_vite import VitePlugin, ViteConfig

from server.db import commit_upon_success

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
    before_send_handler=commit_upon_success,
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


vite_plugin = VitePlugin(
    config=ViteConfig(
        static_dir=PROJECT_ROOT / "frontend",
        templates_dir=PROJECT_ROOT / "server/templates",
        static_url="/src/",
        hot_reload=True,
        port=5000
    )
)

cors_config = CORSConfig(
    allow_origins=["127.0.0.1:5000", "localhost:5000"]
)

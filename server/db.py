from litestar.contrib.sqlalchemy.base import BigIntAuditBase as _BigIntAuditBase
from litestar.contrib.sqlalchemy.base import BigIntBase as _BigIntBase
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite", session_config=session_config
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

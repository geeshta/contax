from collections.abc import AsyncGenerator

from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.config import sqlalchemy_config


sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def provide_transaction(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

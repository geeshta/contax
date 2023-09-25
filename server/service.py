from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from server.logging import Logger
from abc import ABC


class AbstractService(ABC):
    __slots__ = ("db_session", "logger")

    def __init__(self, db_session: AsyncSession, logger: Logger):
        self.db_session = db_session
        self.logger = logger

    @asynccontextmanager
    async def begin_transaction(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with self.db_session.begin():
                yield self.db_session
        except IntegrityError as err:
            self.logger.error(err)
            raise ClientException(status_code=HTTP_409_CONFLICT) from err

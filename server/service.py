from abc import ABC
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.logging import Logger


class AbstractService(ABC):
    __slots__ = ("db_session", "logger")

    def __init__(self, db_session: AsyncSession, logger: Logger):
        self.db_session = db_session
        self.logger = logger

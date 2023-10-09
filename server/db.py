from typing import cast

from advanced_alchemy.extensions.litestar.plugins.init.config.common import (
    SESSION_SCOPE_KEY,
    SESSION_TERMINUS_ASGI_EVENTS,
)
from litestar.constants import HTTP_RESPONSE_START
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from litestar.types import Message, Scope
from litestar.types.asgi_types import HTTPResponseStartEvent
from litestar.utils import delete_litestar_scope_state, get_litestar_scope_state
from sqlalchemy.ext.asyncio import AsyncSession


async def commit_upon_success(message: Message, scope: Scope) -> None:
    session = cast(
        AsyncSession | None, get_litestar_scope_state(scope, SESSION_SCOPE_KEY)
    )
    try:
        if session is not None and message["type"] == HTTP_RESPONSE_START:
            if (
                HTTP_200_OK
                <= cast(HTTPResponseStartEvent, message)["status"]
                < HTTP_400_BAD_REQUEST
            ):
                await session.commit()
            else:
                await session.rollback()
    finally:
        if session and message["type"] in SESSION_TERMINUS_ASGI_EVENTS:
            await session.close()
            delete_litestar_scope_state(scope, SESSION_SCOPE_KEY)

from typing import NotRequired, TypedDict, cast

from litestar import Request

from server.config import session_config

session_middleware = session_config.middleware


class AppSession(TypedDict):
    user_id: NotRequired[int]


async def provide_session(request: Request) -> AppSession:
    return cast(AppSession, request.session)

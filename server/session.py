from collections.abc import MutableMapping
from copy import deepcopy
from typing import Any, Iterator, NotRequired, TypedDict, cast

from litestar import Request
from litestar.middleware.session.client_side import CookieBackendConfig

from server.env import app_config
from server.logging import Logger

session_config = CookieBackendConfig(
    secret=bytes.fromhex(app_config["SECRET"]),
)
session_middleware = session_config.middleware


class AppSession(TypedDict):
    user_id: NotRequired[int]


async def provide_session(request: Request) -> AppSession:
    return cast(AppSession, request.session)

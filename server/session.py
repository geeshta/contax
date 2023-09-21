from collections.abc import MutableMapping
from copy import deepcopy
from typing import Any, Iterator, NotRequired, TypedDict, cast

from litestar import Request
from litestar.middleware.session.client_side import CookieBackendConfig
from picologging import Logger

from server.env import app_config

session_config = CookieBackendConfig(
    secret=bytes.fromhex(app_config["SECRET"]),
)
session_middleware = session_config.middleware


class AppSession(TypedDict):
    user_id: NotRequired[int]


class SessionProxy(MutableMapping):
    def __init__(self, request: Request, logger: Logger):
        self.request = request
        self.logger = logger

    @property
    def session(self) -> AppSession:
        return cast(AppSession, self.request.session)

    @session.setter
    def session(self, value: AppSession) -> None:
        self.request.set_session(value)

    def __getitem__(self, key: str) -> Any:
        return self.session[key]

    def __setitem__(self, key: str, value: Any) -> None:
        new_session = deepcopy(self.session)
        new_session[key] = value
        self.session = new_session

    def __delitem__(self, key: str) -> None:
        new_session = deepcopy(self.session)
        del new_session[key]
        self.session = new_session

    def __iter__(self) -> Iterator[str]:
        return iter(self.session)

    def __len__(self) -> int:
        return len(self.session)


async def provide_session(request: Request, logger: Logger) -> SessionProxy:
    return SessionProxy(request, logger)

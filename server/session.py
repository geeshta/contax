from collections.abc import MutableMapping
from typing import Any, Iterator, Literal, TypeAlias

from litestar import Request

from server.config import session_config

session_middleware = session_config.middleware


SessionKey: TypeAlias = Literal["user_id"]


class AppSession(MutableMapping):
    __slots__ = ("request",)

    def __init__(self, request: Request):
        self.request = request

    def __getitem__(self, key: SessionKey) -> Any:
        return self.request.session[key]

    def __setitem__(self, key: SessionKey, value: Any) -> None:
        self.request.session[key] = value

    def __delitem__(self, key: SessionKey) -> None:
        del self.request.session[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.request.session)

    def __len__(self) -> int:
        return len(self.request.session)


async def provide_session(request: Request) -> AppSession:
    return AppSession(request)

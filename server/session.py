from typing import TypedDict, NotRequired

from litestar.middleware.session.client_side import CookieBackendConfig

from server.env import app_config

session_config = CookieBackendConfig(
    secret=bytes.fromhex(app_config["SECRET"]),
)
session_middleware = session_config.middleware


class AppSession(TypedDict):
    user_id: NotRequired[int]

from litestar import Litestar
from litestar.di import Provide

from server.auth import session_auth
from server.contacts.models import Contact
from server.db import sqlalchemy_plugin
from server.logging import provide_logger
from server.session import session_middleware, provide_session
from server.users.controllers import UserController
from server.users.service import provide_user_service

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin],
    dependencies={
        "logger": Provide(provide_logger),
        "session": Provide(provide_session),
        "user_service": Provide(provide_user_service),
    },
    middleware=[session_middleware],
    on_app_init=[session_auth.on_app_init],
)

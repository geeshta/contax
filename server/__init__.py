from litestar import Litestar
from litestar.di import Provide

from server.auth import session_auth
from server.contacts.models import Contact
from server.db import sqlalchemy_plugin
from server.logging import provide_logger
from server.session import session_middleware
from server.users.controllers import UserController

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin],
    dependencies={"logger": Provide(provide_logger)},
    middleware=[session_middleware],
    on_app_init=[session_auth.on_app_init],
)

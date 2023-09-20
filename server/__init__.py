from litestar import Litestar
from litestar.di import Provide

from server.contacts.models import Contact
from server.db import sqlalchemy_plugin
from server.logging import logger
from server.session import session_middleware
from server.users.controllers import UserController

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin],
    dependencies={"logger": Provide(logger)},
    middleware=[session_middleware],
)

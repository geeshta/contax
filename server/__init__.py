from litestar import Litestar
from server.db import sqlalchemy_plugin
from server.users.controllers import create_user

app = Litestar(
    route_handlers=[create_user],
    plugins=[sqlalchemy_plugin],
)

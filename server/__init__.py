from litestar import Litestar
from server.db import sqlalchemy_plugin
from server.users.controllers import UserController
from server.contacts.models import Contact

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin],
)

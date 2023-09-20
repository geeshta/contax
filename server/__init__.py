from litestar import Litestar
from server.db import sqlalchemy_plugin
from server.users.controllers import create_user
from server.contacts.models import Contact

app = Litestar(
    route_handlers=[create_user],
    plugins=[sqlalchemy_plugin],
)

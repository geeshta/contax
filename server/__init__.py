from litestar import Litestar
from server.controllers import create_user

app = Litestar(
    route_handlers=[create_user],
)

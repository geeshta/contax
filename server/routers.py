from litestar import Router

from server.contacts.controllers import ContactApiController
from server.users.controllers import UserApiController

api_router = Router(
    path="/api", route_handlers=[UserApiController, ContactApiController]
)

from litestar import Router
from server.contacts.controllers import ContactApiController, ContactPageController
from server.users.controllers import UserApiController, UserPageController


api_router = Router(
    path="/api", route_handlers=[UserApiController, ContactApiController]
)

mpa_router = Router(
    path="/page", route_handlers=[UserPageController, ContactPageController]
)

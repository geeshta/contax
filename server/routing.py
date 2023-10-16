from litestar import Router

from server.contacts.controllers import ContactApiController, ContactPageController
from server.users.controllers import UserApiController, UserPageController
from server.error_handlers import handle_not_found

api_router = Router(
    path="/api", route_handlers=[UserApiController, ContactApiController]
)

mpa_router = Router(
    path="/page",
    route_handlers=[UserPageController, ContactPageController],
    exception_handlers={404: handle_not_found},  # type: ignore[assignment]
)

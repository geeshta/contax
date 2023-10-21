from litestar import Router

from server.contacts.controllers import (
    ContactApiController,
    ContactHTMXController,
    ContactPageController,
)
from server.error_handlers import handle_not_found
from server.users.controllers import UserApiController, UserPageController

api_router = Router(
    path="/api", route_handlers=[UserApiController, ContactApiController]
)

mpa_router = Router(
    path="/page",
    route_handlers=[UserPageController, ContactPageController],
    exception_handlers={404: handle_not_found},  # type: ignore[assignment]
)

htmx_router = Router(path="/htmx", route_handlers=[ContactHTMXController])

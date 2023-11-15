from litestar import Router, get
from litestar.response import Template
from pathlib import Path
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

@get("/", exclude_from_auth=True)
async def index() -> Template: 
    return Template("index.html.j2")

@get(["/app", "/app/{path:path}"], exclude_from_auth=True, name="contacts_app")
async def spa(path: Path | None) -> Template:
    return Template("spa.html.j2")

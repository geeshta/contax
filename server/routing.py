from litestar import Router, Request, Response
from litestar.response import Redirect
from litestar.exceptions import NotAuthorizedException
from server.contacts.controllers import ContactApiController, ContactPageController
from server.users.controllers import UserApiController, UserPageController
from litestar.status_codes import HTTP_302_FOUND
from litestar.middleware.exceptions.middleware import create_exception_response


def handle_unauthorized(request: Request, err: NotAuthorizedException) -> Response:
    match request.scope["path"].split("/"):
        case ["", "page", *_]:
            login_url = request.app.route_reverse("login_page")
            return Redirect(login_url, status_code=HTTP_302_FOUND)
        case _:
            err.detail = (
                "Unauthorized access."
                if "session" in err.detail.lower()
                else err.detail
            )
            return create_exception_response(request, err)


api_router = Router(
    path="/api", route_handlers=[UserApiController, ContactApiController]
)

mpa_router = Router(
    path="/page", route_handlers=[UserPageController, ContactPageController]
)

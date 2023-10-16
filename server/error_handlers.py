from litestar import Request, Response
from litestar.exceptions import NotAuthorizedException, NotFoundException
from litestar.middleware.exceptions.middleware import create_exception_response
from litestar.response import Redirect, Template
from litestar.status_codes import HTTP_302_FOUND


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


def handle_not_found(request: Request, err: NotFoundException) -> Response:
    return Template("errors/404.html.j2")

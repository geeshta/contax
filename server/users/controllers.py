from litestar import Controller, Request, get, post
from litestar.dto import DTOData
from litestar.exceptions import NotAuthorizedException, PermissionDeniedException
from litestar.response import Template, Redirect
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_302_FOUND,
    HTTP_403_FORBIDDEN,
)

from server.logging import Logger
from server.session import AppSession
from server.users.dto import UserCreate, UserCreateDTO, UserDTO, UserLogin, UserLoginDTO
from server.users.forms import (
    UserCreateForm,
    UserCreateFormData,
    UserLoginForm,
    UserLoginFormData,
)
from server.users.models import User
from server.users.service import UserService
from server.validation import Validation


class UserApiController(Controller):
    path = "/users"
    return_dto = UserDTO

    @post("/", dto=UserCreateDTO, exclude_from_auth=True)
    async def create_user(
        self,
        data: DTOData[UserCreate],
        user_service: UserService,
        session: AppSession,
        validate: Validation,
    ) -> User:
        if session.get("user_id", None) is not None:
            raise PermissionDeniedException(
                "Must be logged out before registering a new user",
                status_code=HTTP_403_FORBIDDEN,
            )
        user_input = validate(data)
        user = await user_service.create_user(user_input)
        return user

    @post("/login", dto=UserLoginDTO, status_code=HTTP_200_OK, exclude_from_auth=True)
    async def login_user(
        self,
        data: DTOData[UserLogin],
        user_service: UserService,
        session: AppSession,
        validate: Validation,
    ) -> User:
        user_input = validate(data)
        user = await user_service.authenticate_user(
            user_input.email, user_input.password
        )
        session["user_id"] = user.id

        return user

    @post("/logout", status_code=HTTP_204_NO_CONTENT, return_dto=None)
    async def logout_user(self, session: AppSession) -> None:
        session.pop("user_id", None)

        return None

    @get("/me")
    async def get_user(self, request: Request) -> User:
        return request.user


class UserPageController(Controller):
    @get("/login", exclude_from_auth=True, name="login_page")
    async def login_page(self) -> Template:
        form = UserLoginForm()
        return Template(
            template_name="users/login.html.j2",
            context={"form": form},
        )

    @post("/login", exclude_from_auth=True, name="process_login_page")
    async def process_login(
        self,
        data: UserLoginFormData,
        user_service: UserService,
        session: AppSession,
        request: Request,
    ) -> Template | Redirect:
        form = UserLoginForm(data=data)
        if form.validate():
            try:
                user = await user_service.authenticate_user(
                    form.email.data, form.password.data
                )
            except NotAuthorizedException as err:
                form.form_errors.append(err.detail)
                return Template(
                    template_name="users/login.html.j2",
                    context={"form": form},
                )
            else:
                session["user_id"] = user.id
                login_url = request.app.route_reverse("login_page")
                return Redirect(login_url, status_code=HTTP_302_FOUND)
        return Template(
            template_name="users/login.html.j2",
            context={"form": form},
        )

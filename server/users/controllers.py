from litestar import Controller, Request, get, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from litestar.exceptions import PermissionDeniedException

from server.users.dto import UserCreateDTO, UserDTO, UserLoginDTO
from server.users.models import User, UserCreate, UserLogin
from server.users.service import UserService, provide_user_service
from server.session import SessionProxy


class UserController(Controller):
    path = "/users"
    return_dto = UserDTO
    dependencies = {"user_service": Provide(provide_user_service)}

    @post("/", dto=UserCreateDTO, exclude_from_auth=True)
    async def create_user(
        self,
        data: DTOData[UserCreate],
        user_service: UserService,
        session: SessionProxy,
    ) -> User:
        if session.get("user_id", None) is not None:
            raise PermissionDeniedException(
                "Must be logged out before registering a new user",
                status_code=HTTP_403_FORBIDDEN,
            )
        user_input = user_service.validate_input(data)
        user = await user_service.create_user(user_input.email, user_input.password)
        return user

    @post("/login", dto=UserLoginDTO, status_code=HTTP_200_OK, exclude_from_auth=True)
    async def login_user(
        self, data: DTOData[UserLogin], user_service: UserService, session: SessionProxy
    ) -> User:
        user_input = user_service.validate_input(data)
        user = await user_service.authenticate_user(
            user_input.email, user_input.password
        )
        session["user_id"] = user.id

        return user

    @post("/logout", status_code=HTTP_204_NO_CONTENT)
    async def logout_user(self, session: SessionProxy) -> None:
        session.pop("user_id", None)

        return None

    @get("/me")
    async def get_user(self, request: Request) -> User:
        return request.user

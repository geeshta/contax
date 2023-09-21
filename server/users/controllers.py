from litestar import Controller, Request, get, post
from litestar.dto import DTOData
from litestar.exceptions import PermissionDeniedException
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from server.session import SessionProxy
from server.users.dto import UserCreate, UserCreateDTO, UserDTO, UserLogin, UserLoginDTO
from server.users.models import User
from server.users.service import UserService
from server.validation import Validation


class UserController(Controller):
    path = "/users"
    return_dto = UserDTO

    @post("/", dto=UserCreateDTO, exclude_from_auth=True)
    async def create_user(
        self,
        data: DTOData[UserCreate],
        user_service: UserService,
        session: SessionProxy,
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
        session: SessionProxy,
        validate: Validation,
    ) -> User:
        user_input = validate(data)
        user = await user_service.authenticate_user(user_input)
        session["user_id"] = user.id

        return user

    @post("/logout", status_code=HTTP_204_NO_CONTENT, return_dto=None)
    async def logout_user(self, session: SessionProxy) -> None:
        session.pop("user_id", None)

        return None

    @get("/me")
    async def get_user(self, request: Request) -> User:
        return request.user

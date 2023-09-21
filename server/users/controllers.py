from litestar import Controller, post, get
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_200_OK, HTTP_409_CONFLICT
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from litestar import Request
from server.users.dto import UserCreate, UserCreateDTO, UserDTO, UserLogin, UserLoginDTO
from server.users.models import User
from server.users.service import UserService, provide_user_service
from typing import cast
from server.session import AppSession


class UserController(Controller):
    path = "/users"
    return_dto = UserDTO
    dependencies = {"user_service": Provide(provide_user_service)}

    @post("/", dto=UserCreateDTO, exclude_from_auth=True)
    async def create_user(
        self,
        data: DTOData[UserCreate],
        db_session: AsyncSession,
        user_service: UserService,
    ) -> User:
        user_input = user_service.validate_input(data)
        user = user_service.create_user(user_input.email, user_input.password)

        try:
            db_session.add(user)
            await db_session.commit()
        except IntegrityError as err:
            await db_session.rollback()
            raise ClientException(
                f"User with email {user.email} already exists.",
                status_code=HTTP_409_CONFLICT,
            ) from err

        return user

    @post("/login", dto=UserLoginDTO, status_code=HTTP_200_OK, exclude_from_auth=True)
    async def login_user(
        self,
        data: DTOData[UserLogin],
        db_session: AsyncSession,
        user_service: UserService,
        request: Request,
    ) -> User:
        user_input = user_service.validate_input(data)

        query = select(User).where(User.email == user_input.email)
        result = await db_session.execute(query)
        user = user_service.authenticate_user(
            result.scalar_one_or_none(), user_input.password
        )

        session = cast(AppSession, request.session)
        session["user_id"] = user.id
        request.set_session(session)

        return user

    @get("/me")
    async def get_user(self, request: Request) -> User:
        return request.user

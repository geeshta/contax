import json
import logging
from litestar import Controller, post
from litestar.dto import DTOData
from litestar.di import Provide
from litestar.exceptions import ClientException, NotAuthorizedException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.users.dto import UserCreate, UserCreateDTO, UserDTO, UserLogin, UserLoginDTO
from server.users.models import User
from server.users.security import user_security_service, UserSecurityService
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
)


class UserController(Controller):
    path = "/users"
    return_dto = UserDTO
    dependencies = {"user_security_service": Provide(user_security_service)}

    @post("/", dto=UserCreateDTO)
    async def create_user(
        self,
        data: DTOData[UserCreate],
        db_session: AsyncSession,
        user_security_service: UserSecurityService,
    ) -> User:
        try:
            user_input = data.create_instance()
        except ValidationError as err:
            raise ClientException(
                "Validation error while processing body",
                status_code=HTTP_400_BAD_REQUEST,
                extra=json.loads(err.json(include_context=False, include_url=False)),
            ) from err

        password = user_input.password2
        hash_string = user_security_service.hash_password(password)

        user = User(email=user_input.email, password_hash=hash_string)

        try:
            db_session.add(user)
            await db_session.commit()
        except IntegrityError as err:
            await db_session.rollback()
            raise ClientException(
                f"User with email {user.email} already exists.",
                status_code=HTTP_409_CONFLICT,
            )

        return user

    @post("/login", dto=UserLoginDTO, status_code=HTTP_200_OK)
    async def login_user(
        self,
        data: DTOData[UserLogin],
        db_session: AsyncSession,
        user_security_service: UserSecurityService,
    ) -> User:
        try:
            user_input = data.create_instance()
        except ValidationError as err:
            raise ClientException(
                "Validation error while processing body",
                status_code=HTTP_400_BAD_REQUEST,
                extra=json.loads(err.json(include_context=False, include_url=False)),
            ) from err

        query = select(User).where(User.email == user_input.email)
        result = await db_session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise NotAuthorizedException(
                "Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
            )

        is_authenticated = user_security_service.verify_password(
            user_input.password, user.password_hash
        )

        if not is_authenticated:
            raise NotAuthorizedException(
                "Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
            )

        return user

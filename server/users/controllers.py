import json
import logging
from litestar import Controller, post
from litestar.dto import DTOData
from litestar.di import Provide
from litestar.exceptions import ClientException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from server.users.dto import UserCreate, UserCreateDTO, UserDTO
from server.users.models import User
from server.users.security import user_security_service, UserSecurityService


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
                status_code=400,
                extra=json.loads(err.json(include_context=False, include_url=False)),
            ) from err
        else:
            password = user_input.password2
            hash_string = user_security_service.hash_password(password)

            user = User(email=user_input.email, password_hash=hash_string)
            return user

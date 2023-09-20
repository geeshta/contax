import hashlib
import json

from litestar import post
from litestar.dto import DTOData
from litestar.exceptions import ClientException
from pydantic import ValidationError

from server.users.dto import UserCreate, UserCreateDTO, UserDTO, UserMockModel


@post("/users", dto=UserCreateDTO, return_dto=UserDTO)
async def create_user(data: DTOData[UserCreate]) -> UserMockModel:
    try:
        user_input = data.create_instance()
    except ValidationError as err:
        raise ClientException(
            "Validation error while processing body",
            status_code=400,
            extra=json.loads(err.json(include_context=False, include_url=False)),
        ) from err
    password = user_input.password2
    hash = hashlib.sha256(password.encode())
    hex_hash = hash.hexdigest()

    user = UserMockModel(email=user_input.email, password_hash=hex_hash)
    return user

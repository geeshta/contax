from litestar import post
from server.dto import UserCreateDTO, UserDTO, UserMockModel, UserCreate
from litestar.dto import DTOData
import hashlib


@post("/users", dto=UserCreateDTO, return_dto=UserDTO)
async def create_user(data: DTOData[UserCreate]) -> UserMockModel:
    user_input = data.create_instance()
    password = user_input.password2.get_secret_value()
    hash = hashlib.sha256(password.encode())
    hex_hash = hash.hexdigest()

    user = UserMockModel(email=user_input.email, password_hash=hex_hash)
    return user

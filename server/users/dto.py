from litestar.contrib.pydantic import PydanticDTO
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig

from server.users.models import User, UserCreate, UserLogin


class UserCreateDTO(PydanticDTO[UserCreate]):
    config = DTOConfig()


class UserLoginDTO(PydanticDTO[UserLogin]):
    config = DTOConfig()


class UserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(
        exclude={"password_hash", "contacts", "created_at", "updated_at"}
    )

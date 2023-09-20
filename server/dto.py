from pydantic import BaseModel, EmailStr, SecretStr, model_validator
from typing import Self
from litestar.contrib.pydantic import PydanticDTO
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from server.models import User


class UserCreate(BaseModel):
    email: str
    password1: SecretStr
    password2: SecretStr

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if (
            self.password1 is not None
            and self.password2 is not None
            and self.password1 != self.password2
        ):
            raise ValueError("Passwords did not match")

        return self


class UserCreateDTO(PydanticDTO[UserCreate]):
    config = DTOConfig()


# TODO after implementing DB
# class UserDTO(SQLAlchemyDTO[User]):
#     config = DTOConfig(exclude={"password_hash"})


class UserMockModel(BaseModel):
    email: EmailStr
    password_hash: str


class UserDTO(PydanticDTO[UserCreate]):
    config = DTOConfig(exclude={"password_hash"})

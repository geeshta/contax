from typing import TYPE_CHECKING

from email_validator import EmailNotValidError, validate_email
from litestar.contrib.pydantic import PydanticDTO
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from pydantic import BaseModel, field_validator

from server.users.models import User

if TYPE_CHECKING:
    from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    email: str
    password1: str
    password2: str

    @field_validator("email")
    @classmethod
    def check_email_valid(cls, value: str, info: "FieldValidationInfo") -> str:
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format.")

        return value

    @field_validator("password2")
    @classmethod
    def check_passwords_match(cls, value: str, info: "FieldValidationInfo") -> str:
        if info.data["password1"] != value:
            raise ValueError("Passwords did not match.")

        return value


class UserCreateDTO(PydanticDTO[UserCreate]):
    config = DTOConfig()


# TODO after implementing DB
# class UserDTO(SQLAlchemyDTO[User]):
#     config = DTOConfig(exclude={"password_hash"})


class UserMockModel(BaseModel):
    email: str
    password_hash: str


class UserDTO(PydanticDTO[UserMockModel]):
    config = DTOConfig(exclude={"password_hash"})

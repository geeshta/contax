from email_validator import EmailNotValidError, validate_email
from litestar.contrib.pydantic import PydanticDTO
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from server.users.models import User


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def check_email_valid(cls, value: str, info: FieldValidationInfo) -> str:
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format.")

        return value


class UserCreate(UserLogin):
    password2: str

    @field_validator("password2")
    @classmethod
    def check_passwords_match(cls, value: str, info: FieldValidationInfo) -> str:
        if info.data["password"] != value:
            raise ValueError("Passwords did not match.")

        return value


class UserCreateDTO(PydanticDTO[UserCreate]):
    config = DTOConfig()


class UserLoginDTO(PydanticDTO[UserLogin]):
    config = DTOConfig()


class UserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(
        exclude={"password_hash", "contacts", "created_at", "updated_at"}
    )

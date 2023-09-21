from email_validator import EmailNotValidError, validate_email
from litestar.contrib.pydantic import PydanticDTO
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.config import DTOConfig
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from server.contacts.models import Contact


class ContactModel(BaseModel):
    name: str
    phone_number: str | None
    email: str | None

    @field_validator("email")
    @classmethod
    def check_email_valid(
        cls, value: str | None, info: FieldValidationInfo
    ) -> str | None:
        if value is not None:
            try:
                validate_email(value)
            except EmailNotValidError:
                raise ValueError("Invalid email format.")

        return value


class ContactInDTO(PydanticDTO[ContactModel]):
    config = DTOConfig()


class ContactDTO(SQLAlchemyDTO[Contact]):
    config = DTOConfig(exclude={"user", "user_id"})

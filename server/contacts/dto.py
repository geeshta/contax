from email_validator import EmailNotValidError, validate_email
from litestar.contrib.pydantic import PydanticDTO
from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig
from litestar.dto.config import DTOConfig
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from server.contacts.models import Contact


class ContactModel(BaseModel):
    name: str
    phone_number: str | None
    email: str | None

    @field_validator("email")
    @classmethod
    def check_email_valid(cls, value: str | None, info: ValidationInfo) -> str | None:
        if value is not None:
            try:
                validate_email(value)
            except EmailNotValidError:
                raise ValueError("Invalid email format.")

        return value


class ContactInDTO(PydanticDTO[ContactModel]):
    config = DTOConfig()


class ContactDTO(SQLAlchemyDTO[Contact]):
    config = SQLAlchemyDTOConfig(exclude={"user", "user_id"})

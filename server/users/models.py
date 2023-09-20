from typing import TYPE_CHECKING

from email_validator import EmailNotValidError, validate_email
from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from server.contacts.models import Contact

if TYPE_CHECKING:
    from pydantic_core.core_schema import FieldValidationInfo


class User(BigIntAuditBase):
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    contacts = relationship("Contact", back_populates="user", lazy="noload")

    @validates("email")
    def check_email_valid(self, key: str, value: str) -> str:
        try:
            validate_email(value)
        except EmailNotValidError as err:
            raise ValueError("Email not valid!") from err
        return value


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def check_email_valid(cls, value: str, info: "FieldValidationInfo") -> str:
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format.")

        return value


class UserCreate(UserLogin):
    password2: str

    @field_validator("password2")
    @classmethod
    def check_passwords_match(cls, value: str, info: "FieldValidationInfo") -> str:
        if info.data["password"] != value:
            raise ValueError("Passwords did not match.")

        return value

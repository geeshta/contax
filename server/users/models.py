from email_validator import EmailNotValidError, validate_email
from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from server.contacts.models import Contact


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

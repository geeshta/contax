from litestar.contrib.sqlalchemy.base import BigIntAuditBase, BigIntBase
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from email_validator import validate_email, EmailNotValidError


class User(BigIntAuditBase):
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    contacts = relationship("Contact", back_populates="user", lazy="noload")

    @validates("email")
    def validate_this_email(self, key: str, value: str) -> str:
        try:
            validate_email(value)
        except EmailNotValidError as err:
            raise ValueError("Email not valid!") from err
        return value


class Contact(BigIntBase):
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey("user.id"))
    user = relationship(User, back_populates="contacts", lazy="selectin")

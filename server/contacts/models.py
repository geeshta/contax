from litestar.contrib.sqlalchemy.base import BigIntBase
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Contact(BigIntBase):
    name: Mapped[str]
    phone_number: Mapped[str | None]
    email: Mapped[str | None]
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="contacts", lazy="selectin")

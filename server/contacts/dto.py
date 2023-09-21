from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.contrib.pydantic import PydanticDTO
from litestar.dto.config import DTOConfig

from server.contacts.models import Contact
from pydantic import BaseModel


class ContactModel(BaseModel):
    name: str
    phone_number: str | None
    email: str | None


class ContactDTO(SQLAlchemyDTO[Contact]):
    config = DTOConfig()

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto.config import DTOConfig

from server.contacts.models import Contact


class ContactDTO(SQLAlchemyDTO[Contact]):
    config = DTOConfig()

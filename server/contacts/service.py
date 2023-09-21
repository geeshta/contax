from server.logging import Logger
from sqlalchemy.ext.asyncio import AsyncSession
from server.contacts.dto import ContactModel


class ContactService:
    def __init__(
        self, logger: Logger, db_session: AsyncSession, transaction: AsyncSession
    ):
        self.logger = logger
        self.db_session = db_session
        self.transaction = transaction

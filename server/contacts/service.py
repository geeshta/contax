from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_404_NOT_FOUND
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.contacts.dto import ContactModel
from server.contacts.models import Contact
from server.logging import Logger
from server.session import AppSession


class ContactService:
    def __init__(
        self,
        logger: Logger,
        db_session: AsyncSession,
        transaction: AsyncSession,
        session: AppSession,
    ):
        self.logger = logger
        self.db_session = db_session
        self.transaction = transaction
        self.current_user_id = session.get("user_id")

    async def create_contact(self, contact_input: ContactModel) -> Contact:
        contact = Contact(user_id=self.current_user_id, **contact_input.model_dump())
        self.transaction.add(contact)
        await self.transaction.flush()
        return contact

    async def get_user_contacts(self) -> list[Contact]:
        query = select(Contact).where(Contact.user_id == self.current_user_id)
        result = await self.db_session.execute(query)
        contacts = result.scalars().all()
        return list(contacts)

    async def get_user_contact_by_id(self, id: int) -> Contact:
        query = select(Contact).filter(
            Contact.id == id, Contact.user_id == self.current_user_id
        )
        result = await self.db_session.execute(query)
        contact = result.scalar_one_or_none()
        if contact is None:
            raise NotFoundException(
                f"Contact with ID {id} not found.",
                status_code=HTTP_404_NOT_FOUND,
            )
        return contact

    async def update_contact(self, id: int, contact_input: ContactModel) -> Contact:
        contact = await self.get_user_contact_by_id(id)

        for key, value in contact_input.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        await self.transaction.merge(contact)
        return contact

    async def delete_contact(self, id: int) -> None:
        contact = await self.get_user_contact_by_id(id)
        await self.transaction.delete(contact)


async def provide_contact_service(
    logger: Logger,
    db_session: AsyncSession,
    transaction: AsyncSession,
    session: AppSession,
) -> ContactService:
    return ContactService(logger, db_session, transaction, session)

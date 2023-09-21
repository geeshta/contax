from typing import Sequence

from litestar import Controller, Request, delete, get, post, put
from litestar.dto import DTOData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import NotFoundException
from server.contacts.dto import ContactDTO, ContactInDTO, ContactModel
from server.contacts.models import Contact
from server.users.models import User
from server.validation import Validation
from litestar.status_codes import HTTP_404_NOT_FOUND


class ContactController(Controller):
    path = "/contacts"
    dto = ContactInDTO
    return_dto = ContactDTO

    @get("/")
    async def list_contacts(
        self, request: Request, db_session: AsyncSession
    ) -> Sequence[Contact]:
        user: User = request.user
        query = select(Contact).where(Contact.user_id == user.id)
        result = await db_session.execute(query)
        contacts = result.scalars().all()

        return contacts

    @post("/")
    async def create_contact(
        self,
        data: DTOData[ContactModel],
        request: Request,
        db_session: AsyncSession,
        validate: Validation,
    ) -> Contact:
        contact_input = validate(data)
        contact = Contact(
            user_id=request.user.id, **contact_input.model_dump(exclude_unset=True)
        )
        db_session.add(contact)
        await db_session.commit()
        return contact

    @get("/{id:int}")
    async def retrieve_contact(
        self,
        id: int,
        db_session: AsyncSession,
        request: Request,
    ) -> Contact:
        user: User = request.user
        query = select(Contact).filter(Contact.id == id, Contact.user_id == user.id)
        result = await db_session.execute(query)
        contact = result.scalar_one_or_none()
        if contact is None:
            raise NotFoundException(
                f"Contact with ID {id} could not be found",
                status_code=HTTP_404_NOT_FOUND,
            )
        return contact

    @put("/{id:int}")
    async def update_contact(
        self,
        id: int,
        data: DTOData[ContactModel],
        db_session: AsyncSession,
        request: Request,
        validate: Validation,
    ) -> Contact:
        contact_input = validate(data)
        user: User = request.user
        query = select(Contact).filter(Contact.id == id, Contact.user_id == user.id)
        result = await db_session.execute(query)
        contact = result.scalar_one_or_none()
        if contact is None:
            raise NotFoundException(
                f"Contact with ID {id} could not be found",
                status_code=HTTP_404_NOT_FOUND,
            )

        for key, value in contact_input.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        await db_session.commit()
        return contact

    @delete("/{id:int}", dto=None, return_dto=None)
    async def delete_contact(
        self, id: int, db_session: AsyncSession, request: Request
    ) -> None:
        user: User = request.user
        query = select(Contact).filter(Contact.id == id, Contact.user_id == user.id)
        result = await db_session.execute(query)
        contact = result.scalar_one_or_none()
        if contact is None:
            raise NotFoundException(
                f"Contact with ID {id} could not be found",
                status_code=HTTP_404_NOT_FOUND,
            )
        await db_session.delete(contact)
        await db_session.commit()

        return None

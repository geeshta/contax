from litestar import Controller, Request, delete, get, post, put
from litestar.dto import DTOData
from server.contacts.dto import ContactDTO, ContactInDTO, ContactModel
from server.contacts.models import Contact
from server.validation import Validation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.users.models import User
from typing import Sequence


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
    async def retrieve_contact(self, id: int) -> Contact:
        ...

    @put("/{id:int}")
    async def update_contact(
        self, id: int, data: DTOData[ContactModel], validate: Validation
    ) -> Contact:
        ...

    @delete("/{id:int}", dto=None, return_dto=None)
    async def delete_contact(self, id: int) -> None:
        ...

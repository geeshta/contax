from litestar import Controller, delete, get, post, put, Request
from litestar.di import Provide
from litestar.dto import DTOData

from server.contacts.dto import ContactDTO, ContactInDTO, ContactModel
from server.contacts.models import Contact
from server.contacts.service import ContactService, provide_contact_service
from server.validation import Validation
from server.contacts.forms import ContactForm, ContactFormData
from typing import Annotated
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Template, Redirect


class ContactApiController(Controller):
    path = "/contacts"
    dto = ContactInDTO
    return_dto = ContactDTO
    dependencies = {"contact_service": Provide(provide_contact_service)}

    @get("/")
    async def list_contacts(self, contact_service: ContactService) -> list[Contact]:
        contacts = await contact_service.get_user_contacts()

        return contacts

    @post("/")
    async def create_contact(
        self,
        data: DTOData[ContactModel],
        contact_service: ContactService,
        validate: Validation,
    ) -> Contact:
        contact_input = validate(data)
        contact = await contact_service.create_contact(contact_input)

        return contact

    @get("/{id:int}")
    async def retrieve_contact(
        self, id: int, contact_service: ContactService
    ) -> Contact:
        contact = await contact_service.get_user_contact_by_id(id)

        return contact

    @put("/{id:int}")
    async def update_contact(
        self,
        id: int,
        data: DTOData[ContactModel],
        contact_service: ContactService,
        validate: Validation,
    ) -> Contact:
        contact_input = validate(data)
        contact = await contact_service.update_contact(id, contact_input)

        return contact

    @delete("/{id:int}", dto=None, return_dto=None)
    async def delete_contact(self, id: int, contact_service: ContactService) -> None:
        await contact_service.delete_contact(id)

        return None


class ContactPageController(Controller):
    path = "/contacts"
    dependencies = {"contact_service": Provide(provide_contact_service)}

    @get("/", name="contact_list_page")
    async def list_contacts(self, contact_service: ContactService) -> Template:
        return Template("contacts/contact_list.html.j2")

    @post("/")
    async def create_contact(
        self, data: ContactFormData, contact_service: ContactService
    ) -> Template:
        ...

    @get("/{id:int}")
    async def retrieve_contact(
        self, id: int, contact_service: ContactService
    ) -> Template:
        ...

    @post("/{id:int}")
    async def update_contact(
        self,
        id: int,
        data: ContactFormData,
        contact_service: ContactService,
        request: Request,
    ) -> Template | Redirect:
        ...

    @post("/{id:int}/delete")
    async def delete_contact(self, id: int, request: Request) -> Redirect:
        ...

from litestar import Controller, Request, delete, get, post, put
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.response import Redirect, Template
from litestar.status_codes import HTTP_303_SEE_OTHER

from server.contacts.dto import ContactDTO, ContactInDTO, ContactModel
from server.contacts.forms import ContactForm, ContactFormData
from server.contacts.models import Contact
from server.contacts.service import ContactService, provide_contact_service
from server.validation import Validation


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
        contact = await contact_service.create_contact(
            name=contact_input.name,
            phone_number=contact_input.phone_number,
            email=contact_input.email,
        )

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
        contact = await contact_service.update_contact(
            id,
            name=contact_input.name,
            phone_number=contact_input.phone_number,
            email=contact_input.email,
        )

        return contact

    @delete("/{id:int}", dto=None, return_dto=None)
    async def delete_contact(self, id: int, contact_service: ContactService) -> None:
        await contact_service.delete_contact(id)

        return None


class ContactPageController(Controller):
    path = "/contacts"
    dependencies = {"contact_service": Provide(provide_contact_service)}

    async def render_contact_page(
        self, form: ContactForm, contact_service: ContactService
    ):
        contacts = await contact_service.get_user_contacts()
        return Template(
            "contacts/contact_list.html.j2",
            context={"contacts": contacts, "form": form},
        )

    @get("/", name="contact_list_page")
    async def list_contacts(self, contact_service: ContactService) -> Template:
        form = ContactForm()
        return await self.render_contact_page(form, contact_service)

    @post("/", name="process_contact_form")
    async def create_contact(
        self, data: ContactFormData, contact_service: ContactService, request: Request
    ) -> Template | Redirect:
        form = ContactForm(data=data)
        if form.validate():
            await contact_service.create_contact(
                name=form.name.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            contact_page_url = request.app.route_reverse("contact_list_page")
            return Redirect(contact_page_url, status_code=HTTP_303_SEE_OTHER)
        return await self.render_contact_page(form, contact_service)

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

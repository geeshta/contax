from litestar import Controller, Request, delete, get, post, put
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate, HXLocation
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
    include_in_schema = False

    async def render_contact_list_page(
        self, form: ContactForm, contact_service: ContactService
    ) -> Template:
        contacts = await contact_service.get_user_contacts()
        return Template(
            "contacts/contact_list.html.j2",
            context={"contacts": contacts, "form": form},
        )

    async def render_contact_detail_page(
        self, form: ContactForm, contact: Contact
    ) -> Template:
        return Template(
            "contacts/contact_detail.html.j2",
            context={"contact": contact, "form": form},
        )

    @get("/", name="contact_list_page")
    async def list_contacts(self, contact_service: ContactService) -> Template:
        form = ContactForm()
        return await self.render_contact_list_page(
            form=form, contact_service=contact_service
        )

    @post("/", name="process_contact_form")
    async def create_contact(
        self, data: ContactFormData, contact_service: ContactService, request: Request
    ) -> Template | Redirect:
        form = ContactForm(data=data)
        if form.validate():
            await contact_service.create_contact(
                name=form.name.data,  # type: ignore
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            contact_page_url = request.app.route_reverse("contact_list_page")
            return Redirect(contact_page_url, status_code=HTTP_303_SEE_OTHER)
        return await self.render_contact_list_page(form, contact_service)

    @get("/{id:int}", name="contact_detail_page")
    async def retrieve_contact(
        self, id: int, contact_service: ContactService
    ) -> Template:
        contact = await contact_service.get_user_contact_by_id(id)
        form = ContactForm(data=contact.to_dict())
        return await self.render_contact_detail_page(contact=contact, form=form)

    @post("/{id:int}", name="update_contact_form")
    async def update_contact(
        self,
        id: int,
        data: ContactFormData,
        contact_service: ContactService,
        request: Request,
    ) -> Template | Redirect:
        form = ContactForm(data=data)
        if form.validate():
            await contact_service.update_contact(
                id=id,
                name=form.name.data,  # type: ignore
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            return Redirect(
                request.app.route_reverse("update_contact_form", id=id),
                status_code=HTTP_303_SEE_OTHER,
            )
        contact = await contact_service.get_user_contact_by_id(id)
        return await self.render_contact_detail_page(contact=contact, form=form)

    @post("/{id:int}/delete", name="delete_contact")
    async def delete_contact(
        self, id: int, contact_service: ContactService, request: Request
    ) -> Redirect:
        await contact_service.delete_contact(id)
        return Redirect(
            request.app.route_reverse("contact_list_page"),
            status_code=HTTP_303_SEE_OTHER,
        )


class ContactHTMXController(Controller):
    path = "/contacts"
    dependencies = {"contact_service": Provide(provide_contact_service)}
    include_in_schema = False

    async def render_contact_list(self, contact_service: ContactService) -> Template:
        contacts = await contact_service.get_user_contacts()
        return HTMXTemplate(
            template_name="contacts/htmx/contact_list.html.j2",
            context={"contacts": contacts},
        )

    async def render_contact_form(
        self,
        form: ContactForm,
        contact: Contact | None = None,
        re_target: str | None = None,
    ) -> Template:
        return HTMXTemplate(
            re_target=re_target,
            template_name="contacts/htmx/contact_form.html.j2",
            context={"form": form, "contact": contact},
        )

    async def render_contact_detail(self, contact: Contact) -> Template:
        return HTMXTemplate(
            template_name="contacts/htmx/contact_detail.html.j2",
            context={"contact": contact},
        )

    @get("/list", name="contact_list_fragment")
    async def list_contacts(self, contact_service: ContactService) -> Template:
        return await self.render_contact_list(contact_service)

    @get("/form", name="contact_form_fragment")
    async def get_contact_form(self) -> Template:
        form = ContactForm()
        return await self.render_contact_form(form)

    @get("/{id:int}/detail", name="contact_detail_fragment")
    async def get_contact_detail(
        self, id: int, contact_service: ContactService
    ) -> Template:
        contact = await contact_service.get_user_contact_by_id(id)
        return await self.render_contact_detail(contact)

    @get("/{id:int}/form", name="contact_update_form_fragment")
    async def get_contact_update_form(
        self, id: int, contact_service: ContactService
    ) -> Template:
        contact = await contact_service.get_user_contact_by_id(id)
        form = ContactForm(data=contact.to_dict())
        return await self.render_contact_form(form, contact)

    @get("/", name="contact_page_htmx")
    async def contact_page(self) -> Template:
        return Template("contacts/htmx/contact_list_page.html.j2")

    @post("/", name="create_contact_htmx")
    async def create_contact(
        self, data: ContactFormData, contact_service: ContactService
    ) -> Template:
        form = ContactForm(data=data)
        if form.validate():
            await contact_service.create_contact(
                name=form.name.data,  # type: ignore
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            return await self.render_contact_list(contact_service)
        return await self.render_contact_form(form, re_target="#contact-form")

    @get("/{id:int}", name="contact_detail_htmx")
    async def contact_detail(
        self, id: int, contact_service: ContactService
    ) -> Template:
        contact = await contact_service.get_user_contact_by_id(id)
        return Template(
            "contacts/htmx/contact_detail_page.html.j2", context={"contact": contact}
        )

    @put("/{id:int}", name="update_contact_htmx")
    async def update_contact(
        self,
        id: int,
        data: ContactFormData,
        contact_service: ContactService,
    ) -> Template:
        form = ContactForm(data=data)
        if form.validate():
            contact = await contact_service.update_contact(
                id=id,
                name=form.name.data,  # type: ignore
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            return await self.render_contact_detail(contact)
        contact = await contact_service.get_user_contact_by_id(id)
        return await self.render_contact_form(form, contact, re_target="#contact-form")

    @delete("/{id:int}", name="delete_contact_htmx", status_code=200)
    async def delete_contact(
        self, id: int, contact_service: ContactService, request: Request
    ) -> HXLocation:
        await contact_service.delete_contact(id)
        url = request.app.route_reverse("contact_page_htmx")
        return HXLocation(url)

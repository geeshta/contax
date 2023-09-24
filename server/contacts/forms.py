from wtforms import Form
from wtforms.fields import StringField, EmailField
from wtforms.validators import DataRequired, Email
from litestar.params import Body
from litestar.enums import RequestEncodingType
from typing import TypedDict, Required, TypeAlias, Annotated


class ContactDict(TypedDict, total=False):
    name: Required[str]
    phone_number: str | None
    email: str | None


ContactFormData: TypeAlias = Annotated[
    ContactDict, Body(media_type=RequestEncodingType.URL_ENCODED)
]


class ContactForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    phone = StringField("Phone number")
    email = EmailField("Email", validators=[Email(message="Invalid email format")])

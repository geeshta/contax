from typing import Annotated, Required, TypeAlias, TypedDict

from litestar.enums import RequestEncodingType
from litestar.params import Body
from wtforms import Form
from wtforms.fields import EmailField, StringField
from wtforms.validators import DataRequired, Email


class ContactDict(TypedDict, total=False):
    name: Required[str]
    phone_number: str | None
    email: str | None


ContactFormData: TypeAlias = Annotated[
    ContactDict, Body(media_type=RequestEncodingType.URL_ENCODED)
]


class ContactForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    phone_number = StringField("Phone number")
    email = EmailField("Email", validators=[Email(message="Invalid email format")])

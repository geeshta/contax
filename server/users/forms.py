from typing import Annotated, TypeAlias, TypedDict

from litestar.enums import RequestEncodingType
from litestar.params import Body
from wtforms import Form
from wtforms.fields import EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class UserLoginDict(TypedDict):
    email: str
    password: str


class UserCreateDict(UserLoginDict):
    password2: str


UserLoginFormData: TypeAlias = Annotated[
    UserLoginDict, Body(media_type=RequestEncodingType.URL_ENCODED)
]

UserCreateFormData: TypeAlias = Annotated[
    UserCreateDict, Body(media_type=RequestEncodingType.URL_ENCODED)
]


class UserLoginForm(Form):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message="Invalid email format")]
    )
    password = PasswordField("Password", validators=[DataRequired()])


class UserCreateForm(UserLoginForm):
    password2 = PasswordField(
        "Repeat password",
        validators=[
            EqualTo("password", message="Passwords did not match."),
            DataRequired(),
        ],
    )

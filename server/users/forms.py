from typing import TypedDict

from wtforms import Form
from wtforms.fields import EmailField, PasswordField
from wtforms.validators import Email, EqualTo, DataRequired


class UserLoginFormData(TypedDict):
    email: str
    password: str


class UserCreateFormData(UserLoginFormData):
    password2: str


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

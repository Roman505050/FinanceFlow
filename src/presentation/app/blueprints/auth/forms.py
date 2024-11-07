from flask_wtf import FlaskForm  # type: ignore[import-untyped]
from wtforms import (  # type: ignore[import-untyped]
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (  # type: ignore[import-untyped]
    DataRequired,
    Length,
    Email,
    EqualTo,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=100)]
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired(), Length(min=6, max=64)]
    )
    password2 = PasswordField(
        "Підтвердження паролю",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Зареєструватися")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=100)]
    )
    password = PasswordField(
        "Пароль", validators=[DataRequired(), Length(min=6, max=64)]
    )
    submit = SubmitField("Увійти")

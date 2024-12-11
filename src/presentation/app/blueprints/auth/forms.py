from flask_wtf import FlaskForm  # type: ignore[import-untyped]
from wtforms import (  # type: ignore[import-untyped]
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (  # type: ignore[import-untyped]
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message=(
                    "Username must only contain letters, "
                    "numbers, and underscores."
                ),
            ),
        ],
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

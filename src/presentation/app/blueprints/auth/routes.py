from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from pydantic import ValidationError
from loguru import logger

from core.application.user.dto.user import RegisterUserDTO, LoginUserDTO
from core.application.user.exceptions.invalid_credentials import (
    UserInvalidCredentialsException,
)
from core.application.user.factories.user import UserFactory
from core.application.user.use_cases.register import RegisterUserUseCase
from core.application.user.use_cases.login import LoginUserUseCase
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.role import RoleRepository
from core.infrastructure.repositories.user import UserRepository
from core.infrastructure.services.cryptography import CryptographyService
from core.shared.exceptions import AlreadyExistsException
from presentation.app.blueprints.auth.forms import RegistrationForm, LoginForm


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


@auth_bp.route("/login", methods=["GET", "POST"])
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Because mypy thinks that form.data is None
            if form.email.data is None:
                form.email.errors.append("Email is required")
                return render_template("auth/login.html", form=form)
            if form.password.data is None:
                form.password.errors.append("Password is required")
                return render_template("auth/login.html", form=form)

            try:
                login_dto = LoginUserDTO(
                    email=form.email.data,
                    password=form.password.data,
                )
            except ValidationError as e:
                logger.error(e)
                flash("Invalid data", "error")
                return render_template("auth/login.html", form=form)

            cryptography_service = CryptographyService()
            async with SessionContextManager() as db_session:
                user_repo = UserRepository(db_session)
                use_case = LoginUserUseCase(user_repo, cryptography_service)

                try:
                    user_dto = await use_case.execute(login_dto)

                    session["user_id"] = user_dto.user_id
                    session["username"] = user_dto.username
                    session["email"] = user_dto.email
                except UserInvalidCredentialsException as e:
                    flash(str(e), "error")
                    return render_template("auth/login.html", form=form)

            return redirect(url_for("home"))
        except Exception as e:
            logger.error(e)
            flash("Something went wrong", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
async def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Because mypy thinks that form.data is None
            if form.username.data is None:
                form.username.errors.append("Username is required")
                return render_template("auth/login.html", form=form)
            if form.email.data is None:
                form.email.errors.append("Email is required")
                return render_template("auth/login.html", form=form)
            if form.password.data is None:
                form.password.errors.append("Password is required")
                return render_template("auth/login.html", form=form)

            try:
                register_dto = RegisterUserDTO(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                )
            except ValidationError as e:
                logger.error(e)
                flash("Invalid data", "error")
                return render_template("auth/login.html", form=form)

            cryptography_service = CryptographyService()
            user_factory = UserFactory(cryptography_service)
            async with SessionContextManager() as db_session:
                user_repo = UserRepository(db_session)
                role_repo = RoleRepository(db_session)
                use_case = RegisterUserUseCase(
                    user_repo, role_repo, user_factory
                )

                try:
                    user_dto = await use_case.execute(register_dto)

                    session["user_id"] = user_dto.user_id
                    session["username"] = user_dto.username
                    session["email"] = user_dto.email
                except AlreadyExistsException as e:
                    if "email" in str(e).lower():
                        form.email.errors.append(str(e))
                    if "username" in str(e).lower():
                        form.username.errors.append(str(e))
                    return render_template("auth/register.html", form=form)

            return redirect(url_for("home"))
        except Exception as e:
            logger.error(e)
            flash("Something went wrong", "error")
    return render_template("auth/register.html", form=form)

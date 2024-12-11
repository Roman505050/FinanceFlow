from flask import Blueprint, abort, render_template, session

from core.application.user.use_cases.get_user import GetUserUseCase
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.user import UserRepository
from presentation.app.utils.permissions import has_permissions


admin_bp = Blueprint(
    "admin",
    __name__,
)


@admin_bp.before_request
async def check_admin():
    user_id = session.get("user_id")
    if user_id is None:
        abort(404)
    async with SessionContextManager() as db_session:
        user_repository = UserRepository(db_session)
        use_case = GetUserUseCase(user_repository)
        user = await use_case.execute(user_id)
        if not has_permissions(user, ["admin"]):
            abort(404)


@admin_bp.route("")
def admin_home():
    return render_template("admin/home.html")


@admin_bp.route("/categories")
def admin_categories():
    return render_template("admin/categories.html")


@admin_bp.route("/currencies")
def admin_currencies():
    return render_template("admin/currencies.html")


@admin_bp.route("/operations")
def admin_operations():
    return render_template("admin/operations.html")

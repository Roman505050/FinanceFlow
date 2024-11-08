from flask import (
    Blueprint,
    render_template,
    session,
    abort,
)

from core.application.user.use_cases.get_user import GetUserUseCase
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.user import UserRepository
from presentation.app.utils.permissions import has_permissions

admin_bp = Blueprint(
    "admin",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/admin/static",
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
    return render_template("admin.html")

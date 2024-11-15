from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
)


transactions_bp = Blueprint(
    "transactions",
    __name__,
)


@transactions_bp.route("", methods=["GET"])
def transactions_home():
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("auth.login"))

    return render_template("transactions/home.html")

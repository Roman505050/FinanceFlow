from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    session,
)
from flasgger import Swagger  # type: ignore[import-untyped]

from presentation.app.blueprints.admin.routes import admin_bp
from presentation.app.blueprints.auth.routes import auth_bp
from presentation.app.api.operation import operation_api_bp
from presentation.app.api.category import category_api_bp
from presentation.app.api.currency import currency_api_bp
from config import SESSION_SECRET_KEY

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY

swagger = Swagger(app)
app.register_blueprint(auth_bp, url_prefix="")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(operation_api_bp, url_prefix="/api/v1/operation")
app.register_blueprint(category_api_bp, url_prefix="/api/v1/category")
app.register_blueprint(currency_api_bp, url_prefix="/api/v1/currency")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html", hide_nav=True), 404


@app.route("/")
def home():  # put application's code here
    return render_template("home.html")


@app.route("/transactions")
def expense():
    email = session.get("email")

    if email is None:
        return redirect(url_for("auth.login"))

    return render_template("transactions.html")


@app.route("/statistics")
def chart():
    email = session.get("email")

    if email is None:
        return redirect(url_for("auth.login"))

    return render_template("statistics.html")


if __name__ == "__main__":
    app.run(debug=True)

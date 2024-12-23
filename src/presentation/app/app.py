from asgiref.wsgi import WsgiToAsgi
from flasgger import Swagger  # type: ignore[import-untyped]
from flask import Flask, redirect, render_template, session, url_for

from config import SESSION_SECRET_KEY
from presentation.app.api.category import category_api_bp
from presentation.app.api.currency import currency_api_bp
from presentation.app.api.operation import operation_api_bp
from presentation.app.api.transaction import transaction_api_bp
from presentation.app.blueprints.admin.routes import admin_bp
from presentation.app.blueprints.auth.routes import auth_bp
from presentation.app.blueprints.transactions.routes import transactions_bp


app = Flask(__name__)
app.json.ensure_ascii = False  # type: ignore[attr-defined]
app.secret_key = SESSION_SECRET_KEY

swagger = Swagger(app)
app.register_blueprint(auth_bp, url_prefix="")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(transactions_bp, url_prefix="/transactions")
app.register_blueprint(operation_api_bp, url_prefix="/api/v1/operations")
app.register_blueprint(category_api_bp, url_prefix="/api/v1/categories")
app.register_blueprint(currency_api_bp, url_prefix="/api/v1/currencies")
app.register_blueprint(transaction_api_bp, url_prefix="/api/v1/transactions")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html", hide_nav=True), 404


@app.route("/")
def home():  # put application's code here
    return render_template("home.html")


@app.route("/statistics")
def chart():
    email = session.get("email")

    if email is None:
        return redirect(url_for("auth.login"))

    return render_template("statistics.html")


asgi_app = WsgiToAsgi(app)

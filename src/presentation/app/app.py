from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    session,
)
from jinja2 import FileSystemLoader, ChoiceLoader

from presentation.app.blueprints.auth.routes import auth_bp
from config import SESSION_SECRET_KEY

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY

app.register_blueprint(auth_bp, url_prefix="")


app.jinja_env.loader = ChoiceLoader(
    [
        FileSystemLoader("src/presentation/app/templates"),
        FileSystemLoader("presentation/app/templates"),
        FileSystemLoader("src/presentation/app/blueprints/auth/templates"),
        FileSystemLoader("presentation/app/blueprints/auth/templates"),
    ]
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", hide_nav=True), 404


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

from flask import redirect, request, Blueprint
from flask_login import login_required, logout_user

from flaskr.logic.loginlgc import LoginLogic

login_blueprint = Blueprint('login', __name__)
handler = LoginLogic()


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    return handler.login(request)


@login_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    return handler.signup(request)


@login_blueprint.route("/signup/<token>", methods=["GET", "POST"])
def signup_token(token):
    return handler.signup_token(request, token)


@login_blueprint.route("/confirm/<token>")
def confirm_email(token):
    logout_user()
    return handler.confirm_email(token)


@login_blueprint.route("/forgot-my-password", methods=["GET", "POST"])
def reset_password_via_email():
    return handler.reset_password_via_email(request)


@login_blueprint.route("/forgot-my-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    return handler.reset_password(request, token)


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")

from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
import logging
from logic.loginlgc import LoginLogic

login_blueprint = Blueprint('login', __name__)
handler = LoginLogic()


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    return handler.login(request)

@login_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    return handler.signup(request)


@login_blueprint.route("/confirm/<token>")
def confirm_email(token):
    logout_user()
    return handler.confirm_email(token)


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")
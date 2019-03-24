from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/")
@index_blueprint.route("/home")
def home():
    return render_template("index.html")

@index_blueprint.route("/terms-conditions")
def terms_condititons():
    return render_template("terms_conditions.html")

@index_blueprint.route("/dashboard")
@login_required
def dashboard():
    # if he is a mentor redirect to mentor
    # else if he is a mentee redirect to mentee
    # else {admin} redirect to admin page
    priv = current_user.priv
    if priv == 'system_admin':
        return redirect('/system/admin')
    elif priv == 'admin':
        return redirect('/admin')
    else:
        role = current_user.role
        if role == 'mentee':
            return redirect('/mentee')
        elif role == 'mentor':
            return redirect('/mentor')

    return redirect('/')

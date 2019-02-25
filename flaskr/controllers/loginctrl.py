import basic as db
from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from forms import LoginForm, RegistrationForm
import json
from permissions import permissioned_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from auth_token import verify_token
import requests
from user import User
from werkzeug.security import check_password_hash, generate_password_hash
from emailer import send_email, send_email_confirmation_to_user
import controllers.adminctrl as adminctrl
import logging

login_blueprint = Blueprint('login', __name__)
SECRET_KEY = "powerful secretkey"
EMAIL_CONFIRMATION_EXPIRATION = 86400


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)

    if login_form.login_submit.data: # if the login form was submitted
        if login_form.validate_on_submit(): # if the form was valid
            user = User(login_form.k_number.data)

            # if user exists in db then a password hash was successfully retrieved
            if(user.password):
                # check if he is authorised
                if check_password_hash(user.password, login_form.password.data):
                    # redirect to profile page, where he must insert his preferences
                    login_user(user, remember=False)
                    return redirect("/dashboard")
                else:
                    flash('The password you entered is incorrect')
                    return redirect("/login")
            else:
                return redirect("/login")
        else:
            flash("Error logging in, please check the data that was entered")
            return render_template("login.html", login_form=login_form)

    return render_template("login.html", login_form=login_form)

@login_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    registration_form = RegistrationForm(request.form)

    # if current_user.is_authenticated:
    #     return "Please logout before trying to signup"

    if registration_form.registration_submit.data: # if the registation form was submitted
        if registration_form.validate_on_submit(): # if the form was valid
            # hash the user password
            first_name = registration_form.first_name.data
            last_name = registration_form.last_name.data
            k_number = registration_form.k_number.data
            is_mentor = registration_form.is_mentor.data
            # hashed_password = generate_password_hash(registration_form.password.data)
            hashed_password = generate_password_hash("12345678", method="sha256")

            db_insert_success = db.insert_student(k_number, first_name, last_name, "na", 2018, "na", (1 if is_mentor else 0), hashed_password, False)
            #app.logger.warning("register user: " + k_number)
            user = User(k_number)

            #app.logger.warning("user's knumber: " + user.k_number)
            send_email_confirmation_to_user(user=user, secret_key=SECRET_KEY)

            #app.logger.warning("register user: " + str(db_insert_success))

            #redirect to profile page, where he must insert his preferences
            return redirect("/dashboard")
        else:
            flash("Error logging in, please check the data that was entered correctly")
            return render_template("signup.html", registration_form=registration_form)

    return render_template("signup.html", registration_form=registration_form)


@login_blueprint.route("/confirm/<token>")
def confirm_email(token):
    logout_user()
    k_number = verify_token(secret_key=SECRET_KEY, token=token, expiration=EMAIL_CONFIRMATION_EXPIRATION)

    if k_number:
        # return "this is: " + str(k_number)
        user = User(k_number)
        if user.email_confirmed:
            return "account already active"
        else:
            user.activate()
            return "account activated"
    else:
        #app.logger.warning("token verification failed")
        return "token verification fail"



@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")
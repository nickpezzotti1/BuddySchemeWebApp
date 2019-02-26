from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from auth_token import verify_token
from user import User
from werkzeug.security import check_password_hash, generate_password_hash
from emailer import send_email, send_email_confirmation_to_user
import logging
from models.studentmdl import StudentModel


class LoginLogic():

    SECRET_KEY = "powerful secretkey"
    EMAIL_CONFIRMATION_EXPIRATION = 86400

    def login(self, request):

        try:
            login_form = LoginForm(request.form)

        except Exception as e:
            self._log.exception("Invalid login form")
            return abort(404)

        try:

            if login_form.login_submit.data: 
                if login_form.validate_on_submit():
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

        except Exception as e:
            self._log.exception("Could not parse login form")
            return abort(404)

    
    def signup(self,request):

        try:
            registration_form = RegistrationForm(request.form)

        except Exception as e:
            self._log.exception("Invalid registration form")
            return abort(404)

        try:
            if registration_form.registration_submit.data: # if the registation form was submitted
                if registration_form.validate_on_submit(): # if the form was valid
                    # hash the user password
                    first_name = registration_form.first_name.data
                    last_name = registration_form.last_name.data
                    k_number = registration_form.k_number.data
                    is_mentor = registration_form.is_mentor.data
                    # hashed_password = generate_password_hash(registration_form.password.data)
                    hashed_password = generate_password_hash("12345678", method="sha256")

                    db_insert_success = self._student_handler.insert_student(k_number, first_name, last_name, "na", 2018, "na", (1 if is_mentor else 0), hashed_password, False)
                    #app.logger.warning("register user: " + k_number)
                    user = User(k_number)

                    #app.logger.warning("user's knumber: " + user.k_number)
                    send_email_confirmation_to_user(user=user, secret_key=self.SECRET_KEY)

                    #app.logger.warning("register user: " + str(db_insert_success))

                    #redirect to profile page, where he must insert his preferences
                    return redirect("/dashboard")
                else:
                    flash("Error logging in, please check the data that was entered correctly")
                    return render_template("signup.html", registration_form=registration_form)

            return render_template("signup.html", registration_form=registration_form)

        except Exception as e:
            self._log.exception("Could not parse registration form")
            return abort(404)


    def confirm_email(self,token):

        try:
            k_number = verify_token(secret_key=self.SECRET_KEY, token=token, expiration=self.EMAIL_CONFIRMATION_EXPIRATION)
        
        except Exception as e:
            self._log.exception("Could not verify token")
            return abort(404)

        try:
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

        except Exception as e:
            self._log.exception("Could not activate account")
            return abort(404)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._student_handler = StudentModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(404)


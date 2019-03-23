from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort, current_app
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from auth_token import verify_token
from user import Student
from werkzeug.security import check_password_hash, generate_password_hash
from emailer import send_email, send_email_confirmation_to_user
import logging
from models.studentmdl import StudentModel
from models.schememdl import SchemeModel

class LoginLogic():


    def login(self, request):

        if current_user.is_authenticated:
            return redirect("/dashboard")

        try:
            schemes = self._scheme_handler.get_active_scheme_data()
            scheme_options = [(s['scheme_id'], s['scheme_name']) for s in schemes]

            login_form = LoginForm(request.form)
            login_form.scheme_id.choices = scheme_options

        except Exception as e:
            self._log.exception("Invalid login form")
            flash("Error logging in, please check the data that was entered")
        try:
            if login_form.login_submit.data:
                if login_form.validate_on_submit():
                    try:
                        user = Student(login_form.scheme_id.data, login_form.k_number.data)
                    except:
                        flash('You must first confirm your email address')
                        return redirect("/login")

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
            flash("Oops... Something went wrong. The data entered could not be valid, try again.")

    def signupToken(self, request, token):
        schemeId = verify_token(secret_key=current_app.config["SECRET_KEY"], token=token, expiration=1337331)
        # return schemeId
        return self.signup(request, schemeId=schemeId)


    def signup(self, request, schemeId = False):

        try:
            schemes = self._scheme_handler.get_active_scheme_data()

            if schemeId:
                scheme_options = [(s['scheme_id'], s['scheme_name']) for s in schemes if (s['scheme_id'] == int(schemeId)) ]
            else:
                scheme_options = [(s['scheme_id'], s['scheme_name']) for s in schemes]

            registration_form = RegistrationForm(request.form)
            registration_form.scheme_id.choices = scheme_options

        except Exception as e:
            self._log.exception("Invalid registration form")
            return abort(500)

        try:
            if registration_form.registration_submit.data: # if the registation form was submitted
                if (registration_form.password.data != registration_form.confirm_password.data):
                    flash("Password don't match. Make sure the 'password' and 'confirm passowrd' fields match")
                    return render_template("signup.html", registration_form=registration_form)

                if registration_form.validate_on_submit(): # if the form was valid
                    # hash the user password
                    scheme_id = registration_form.scheme_id.data
                    first_name = registration_form.first_name.data
                    last_name = registration_form.last_name.data
                    k_number = registration_form.k_number.data
                    is_mentor = registration_form.is_mentor.data
                    hashed_password = generate_password_hash(registration_form.password.data)

                    if self._student_handler.user_exist(scheme_id, k_number):
                        flash("User already exists")
                        return render_template("signup.html", registration_form=registration_form)

                    db_insert_success = self._student_handler.insert_student(scheme_id, k_number, first_name, last_name, "na", 2018, "Prefer not to say", (1 if is_mentor else 0), hashed_password, False, 1)
                    #app.logger.warning("register user: " + k_number)
                    user = Student(scheme_id, k_number)
                    print(user.k_number)
                    #app.logger.warning("user's knumber: " + user.k_number)
                    send_email_confirmation_to_user(user=user, secret_key=current_app.config["SECRET_KEY"])

                    #app.logger.warning("register user: " + str(db_insert_success))

                    #redirect to profile page, where he must insert his preferences
                    return redirect("/dashboard")
                else:
                    flash("Error logging in, please check the data that was entered correctly")
                    return render_template("signup.html", registration_form=registration_form)

            return render_template("signup.html", registration_form=registration_form)

        except Exception as e:
            self._log.exception("Could not parse registration form")
            return abort(500)


    def confirm_email(self,token): ### add scheme_id

        try:
            message = verify_token(secret_key=current_app.config["SECRET_KEY"], token=token, expiration=current_app.config["EMAIL_CONFIRMATION_EXPIRATION"])

        except Exception as e:
            self._log.exception("Could not verify token")
            return abort(403)

        try:
            if message:
                print(message)
                print(current_app.config["MESSAGE_SEPARATION_TOKEN"])
                (k_number, scheme_id) = message.split(current_app.config["MESSAGE_SEPARATION_TOKEN"])
                # return "this is: " + str(k_number)
                user = Student(k_number=k_number, scheme_id=scheme_id)
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
            return abort(500)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._student_handler = StudentModel()
            self._scheme_handler = SchemeModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(500)

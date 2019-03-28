import logging

from flask import flash, redirect, render_template, abort, current_app
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth_token import verify_token
from flaskr.emailer import send_email_confirmation_to_user, send_email_reset_password
from flaskr.forms import LoginForm, RegistrationForm, RequestEmailPasswordResetForm, ResetPasswordWithEmailForm
from flaskr.models.schememdl import SchemeModel
from flaskr.models.studentmdl import StudentModel
from flaskr.user import Student


class LoginLogic:

    def login(self, request):
        """

        :param request:
        :return:
        """
        if current_user.is_authenticated:
            return redirect("/dashboard")

        try:
            scheme_options = self._get_scheme()

        except Exception as e:
            self._log.exception("Invalid login form")
            flash("Error logging in, please check the data that was entered")

        login_form = LoginForm(request.form)
        login_form.scheme_id.choices = scheme_options
        try:
            if request.method == "POST":
                if login_form.validate_on_submit():
                    scheme_id = login_form.scheme_id.data
                    k_number = login_form.k_number.data

                    if not self._student_handler.user_exist(scheme_id, k_number):
                        flash("This k_number and password combination does not exist in our database.")
                        return redirect("/login")

                    try:
                        user = Student(scheme_id, k_number)
                    except:
                        flash('You must first confirm your email address')
                        return redirect("/login")

                    # if user exists in db then a password hash was successfully retrieved
                    if user.password:
                        # check if he is authorised
                        if check_password_hash(user.password, login_form.password.data):
                            # redirect to profile page, where he must insert his preferences
                            login_user(user, remember=False)

                            is_mentor = self._student_handler.get_user_data(scheme_id,
                                                                            k_number)['is_mentor']

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

    def signup(self, request, scheme_id=False):
        """

        :param request:
        :param scheme_id:
        :return:
        """
        try:
            if scheme_id:
                schemes = self._scheme_handler.get_active_scheme_data()
                scheme_options = [(s['scheme_id'], s['scheme_name'])
                                  for s in schemes if (s['scheme_id'] == int(scheme_id))]
            else:
                scheme_options = self._get_scheme()

            registration_form = RegistrationForm(request.form)
            registration_form.scheme_id.choices = scheme_options

        except Exception as e:
            self._log.exception("Invalid registration form")
            return abort(500)

        try:
            if request.method == "POST":  # if the registation form was submitted
                if registration_form.password.data != registration_form.confirm_password.data:
                    flash("Password don't match. Make sure the 'password' and 'confirm passowrd' fields match")
                    return render_template("signup.html", registration_form=registration_form)

                if registration_form.validate_on_submit():  # if the form was valid
                    scheme_id = registration_form.scheme_id.data
                    first_name = registration_form.first_name.data
                    last_name = registration_form.last_name.data
                    k_number = registration_form.k_number.data
                    is_mentor = registration_form.is_mentor.data
                    hashed_password = generate_password_hash(registration_form.password.data)

                    if self._student_handler.user_exist(scheme_id, k_number):
                        flash("User already exists")
                        return render_template("signup.html", registration_form=registration_form)

                    self._student_handler.insert_student(
                        scheme_id, k_number, first_name, last_name, "na", 2018, "Prefer not to say",
                        (1 if is_mentor else 0), hashed_password, False, 1)
                    # user = Student(scheme_id, k_number)
                    # print(user.k_number)
                    send_email_confirmation_to_user(
                        scheme_id=scheme_id, k_number=k_number,
                        secret_key=current_app.config["SECRET_KEY"])

                    # redirect to profile page, where he must insert his preferences
                    return redirect("/dashboard")
                else:
                    flash("Error logging in, please check the data that was entered correctly")
                    return render_template("signup.html", registration_form=registration_form)

            return render_template("signup.html", registration_form=registration_form)

        except Exception as e:
            self._log.exception("Could not parse registration form")
            return abort(500)

    def confirm_email(self, token):
        """

        :param token:
        :return:
        """
        try:
            message = verify_token(
                secret_key=current_app.config["SECRET_KEY"],
                expiration=current_app.config["EMAIL_CONFIRMATION_EXPIRATION"],
                token=token)

        except Exception as e:
            self._log.exception("Could not verify token")
            return abort(403)

        try:
            if message:
                (k_number, scheme_id) = message.split(
                    current_app.config["MESSAGE_SEPARATION_TOKEN"])
                
                user = Student(k_number=k_number, scheme_id=scheme_id)

                if user.email_confirmed:
                    flash("Account already active.")
                else:
                    user.activate()
                    flash("Account successfully activated.")
            else:
                flash("The token verification has failed")

        except Exception as e:
            self._log.exception("Could not activate account")
            return abort(500)
        return redirect("/login")

    def _get_scheme(self):
        """

        :return:
        """
        schemes = self._scheme_handler.get_active_scheme_data()
        scheme_options = [(s['scheme_id'], s['scheme_name']) for s in schemes]

        return scheme_options

    def signup_token(self, request, token):
        """

        :param request:
        :param token:
        :return:
        """
        scheme_id = verify_token(
        secret_key=current_app.config["SECRET_KEY"], token=token, expiration=1337331)

        return self.signup(request, scheme_id=scheme_id)

    def reset_password_via_email(self, request):
        """

        :param request:
        :return:
        """
        reset_form = RequestEmailPasswordResetForm(request.form)

        reset_form.scheme_id.choices = self._get_scheme()

        if request.method == "POST":
            if reset_form.validate_on_submit():
                k_number = reset_form.k_number.data
                scheme_id = reset_form.scheme_id.data
                
                flash("If your email exists in our database, you will receive an email. Don't forget to check spam")

                if self._student_handler.user_exist(scheme_id, k_number):
                    send_email_reset_password(k_number=k_number, scheme_id=scheme_id, secret_key=current_app.config["SECRET_KEY"])

        return render_template("request_password_reset.html", reset_form=reset_form)
    
    def reset_password(self, request, token):
        """

        :param request:
        :param token:
        :return:
        """
        reset_password_form = ResetPasswordWithEmailForm(request.form)
        message = verify_token(
                secret_key=current_app.config["SECRET_KEY"],
                expiration=current_app.config["EMAIL_CONFIRMATION_EXPIRATION"],
                token=token)
        
        try:
            (k_number, scheme_id) = message.split(
                        current_app.config["MESSAGE_SEPARATION_TOKEN"])

            if not self._student_handler.user_exist(scheme_id, k_number):
                flash("Invalid link")
                return redirect("/forgot-my-password")

            if request.method == "POST":
                if reset_password_form.validate_on_submit():
                    new_password = reset_password_form.password.data
                    new_hashed_password = generate_password_hash(new_password)
                    self._student_handler.update_hash_password(scheme_id, k_number, new_hashed_password)
                    flash("Password updated successfully")
                    return redirect("/login")

        except Exception as e:
            raise abort(500)
        return render_template("reset_password.html", reset_password_form=reset_password_form)
        

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._student_handler = StudentModel()
            self._scheme_handler = SchemeModel()
        except Exception as e:
            self._log.exception("Could not create model instance")
            raise abort(500)

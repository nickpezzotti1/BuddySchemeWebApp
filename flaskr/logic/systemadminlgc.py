import logging
from os import urandom
import base64

from flask import abort
from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.forms import NewSchemeForm
from flaskr.forms import SystemLoginForm
from flaskr.forms import SchemeFeedbackForm
from flaskr.models.schememdl import SchemeModel
from flaskr.models.studentmdl import StudentModel
from flaskr.user import SystemAdmin
from flaskr.emailer import send_email_scheme_feedback


class SystemAdminLogic:

    def system_admin_login(self, request):
        """
        Produces the sytem admin login html page or a redirect to system admin dashboard if login is successfull
             
        :param request: Login form
        :return: html view
        """
        if current_user.is_authenticated:
            return redirect("/dashboard")

        try:

            system_login_form = SystemLoginForm(request.form)

        except Exception:
            self._log.exception("Invalid login form")
            return abort(500)
        try:
            if system_login_form.submit.data:
                if system_login_form.validate_on_submit():
                    system_admin = SystemAdmin(system_login_form.email.data)
                    if system_admin.password:
                        # check if he is authorised
                        if check_password_hash(system_admin.password, system_login_form.password.data):
                            # redirect to profile page, where he must insert his preferences

                            login_user(system_admin, remember=False)
                            return redirect("/dashboard")
                        else:
                            flash('The password you entered is incorrect')
                            return redirect('/system')
                    else:
                        return redirect('/system')
                else:
                    flash("Error logging in, please check the data that was entered")
                    return render_template("system_admin/login.html", system_login_form=system_login_form)

            return render_template("system_admin/login.html", system_login_form=system_login_form)

        except Exception:
            self._log.exception("Could not parse login form")
            flash("Error logging in, please check the data that was entered")

    def system_admin_dashboard(self):
        """
        Produces the system admin dashboard and handles redirects from requests
        
        :return: html view
        """
        # try:
        if request.method == 'POST' and 'feedbackScheme' in request.form:
            scheme_id = request.form['scheme_id']
            return redirect(url_for('systemadmin.system_scheme_feedback', scheme_id=scheme_id))
        if request.method == 'POST' and 'susScheme' in request.form:
            scheme_id = request.form['scheme_id']
            self._scheme_handler.suspend_scheme(scheme_id)
        elif request.method == 'POST' and 'delScheme' in request.form:
            scheme_id = request.form['scheme_id']
            self._scheme_handler.delete_scheme(scheme_id)

        schemes = self._scheme_handler.get_all_scheme_data()
        return render_template('system_admin/dashboard.html', title='System Admin', schemes=schemes)

    def system_new_scheme(self, request):
        """
        Produces the new scheme page and creates a new scheme upon valid form 
        submission, displaying the scheme admin password on screen

        :param request: new scheme form
        :return: html view
        """
        try:
            new_scheme_form = NewSchemeForm(request.form)

        except Exception:
            self._log.exception("Invalid New Scheme Form")
            return abort(500)

        try:

            if new_scheme_form.submit.data:
                if new_scheme_form.validate_on_submit():
                    new_scheme_name = new_scheme_form.scheme_name.data + \
                        " " + str(new_scheme_form.year.data)
                    if self._scheme_handler.check_scheme_avail(new_scheme_name):
                        if self._scheme_handler.create_new_scheme(new_scheme_name):
                            scheme_admin_k_number = new_scheme_form.k_number.data
                            scheme_id = self._scheme_handler.get_scheme_id(new_scheme_name)
                            random = urandom(10)
                            password = base64.b64encode(random).decode("utf-8")
                            hashed_password = generate_password_hash(password)
                            if self._student_handler.insert_student(scheme_id, scheme_admin_k_number, 'admin change', 'admin change', 'admin change', 2, 'admin change', 1, hashed_password, 1, 1):
                                if self._scheme_handler.create_allocation_config_entry(scheme_id):
                                    flash("Scheme And Admin Account Succesfully Created \n Admin Should Sign In With Password - " + password)
                                else:
                                    flash(
                                        "Scheme And Admin Account Created But Failed To Create Allocation Config")

                            else:
                                flash(
                                    "Scheme Created But Admin Account Failed To Create, Please Manually Assign")

                        else:
                            flash("Database Error Creating New Scheme")
                    else:
                        flash("Scheme Already Exists")

            return render_template('system_admin/new_scheme.html', title='New Scheme', new_scheme_form=new_scheme_form)

        except Exception:
            self._log.exception("Error Creating New Scheme")
            return abort(500)

    def system_view_scheme_dashboard(self, request):
        """
        Redirects to admin dashboard of the selected scheme

        :param request: scheme selection form
        :return: redirect to html view
        """
        if request.method == 'POST' and 'scheme_id' in request.form:
            scheme_id = request.form['scheme_id']
            current_user.set_scheme_id(scheme_id)
            resp = make_response(redirect('/admin'))
            resp.set_cookie('scheme', scheme_id)
            return resp

        else:
            return redirect('/system')

    def system_scheme_feedback(self, request, scheme_id):
        """
        Generates a form and upon submission sends a feeback url to scheme members

        :param request: request form with url for feedback
        :param scheme_id: scheme id to send url to
        :return: html view 
        """
        feedback_form = SchemeFeedbackForm(request.form)

        if request.method == 'POST':
            if feedback_form.validate_on_submit:
                users = self._student_handler.get_all_students_data_basic(scheme_id=scheme_id)
                k_numbers = [i["k_number"] for i in users]
                send_email_scheme_feedback(k_numbers, feedback_url=feedback_form.feedback_form_url.data)
                flash("Email sent to " + str(len(k_numbers)) + " students.")
                    
        return render_template('system_admin/feedback.html', title='Scheme Feedback', feedback_form=feedback_form)

    def __init__(self):
        """

        """
        try:
            self._log = logging.getLogger(__name__)
            self._scheme_handler = SchemeModel()
            self._student_handler = StudentModel()
        except Exception:
            self._log.exception("Could not create model instance")
            return abort(500)

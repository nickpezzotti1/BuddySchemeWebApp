from flask import Blueprint
from flask import Flask
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from forms import NewSchemeForm
import json
import logging
from models.schememdl import SchemeModel
from models.studentmdl import StudentModel
from os import urandom
import requests
from werkzeug.security import generate_password_hash

class SystemAdminLogic():
    
    
    def system_admin_dashboard(self):
        schemes = self._scheme_handler.get_all_scheme_data()
        return render_template('system_admin/dashboard.html', title='System Admin', schemes=schemes)

    def system_new_scheme(self):
        ##require system admin
        try:
            new_scheme_form = NewSchemeForm(request.form)
            
        except Exception as e:
            self._log.exception("Invalid New Scheme Form")
            return abort(500)
        
        try:
        
            if new_scheme_form.submit.data:
                if new_scheme_form.validate_on_submit():
                    new_scheme_name = new_scheme_form.scheme_name.data + " " + str(new_scheme_form.year.data)
                    if self._scheme_handler.check_scheme_avail(new_scheme_name):                        
                        print(new_scheme_name)
                        if self._scheme_handler.create_new_scheme(new_scheme_name):
                            scheme_admin_k_number = new_scheme_form.k_number.data
                            scheme_id = self._scheme_handler.get_scheme_id(new_scheme_name) ## return from create_new_scheme isntead?
                            ##
                            ## ToDo - below
                            ## 
                            password = urandom(16) ## send in email + force to change
                            hashed_password = generate_password_hash(password)
                            if self._student_handler.insert_student(scheme_id, scheme_admin_k_number, 'admin change', 'admin change', 'admin change', 2, 'admin change', 1, hashed_password, 1, 1): ## check res?
                                flash("Scheme And Admin Account Succesfully Created")
                            else:
                                flash("Scheme Created But Admin Account Failed To Create, Please Manually Assign")
                            
                        else:
                            flash("Database Error Creating New Scheme")
                    else:
                        flash("Scheme Already Exists")
                        
            return render_template('system_admin/new_scheme.html', title='New Scheme', new_scheme_form=new_scheme_form)

        except Exception as e:
            self._log.exception("Error Creating New Scheme")
            return abort(500)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._scheme_handler = SchemeModel()
            self._student_handler = StudentModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(404)
        
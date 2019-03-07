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
from forms import NewSchemeForm, SystemLoginForm
import json
import logging
from models.schememdl import SchemeModel
from models.studentmdl import StudentModel
from os import urandom
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from user import SystemAdmin
from permissions import system_admin_login_required

class SystemAdminLogic():
    
    def system_admin_login(self, request):
        ##if current_user.is_authenticated: 
        ##    return redirect("/dashboard")

        try:
            
            system_login_form = SystemLoginForm(request.form)
                
        except Exception as e:
            self._log.exception("Invalid login form")
            return abort(500)

        try:
            if system_login_form.submit.data:
                if system_login_form.validate_on_submit():
                    system_admin = SystemAdmin(system_login_form.email.data)
                    if(system_admin.password):
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

        except Exception as e:
            self._log.exception("Could not parse login form")
            return abort(404)
        
        
    @system_admin_login_required()
    def system_admin_dashboard(self):
        ## try:
        if(request.method == 'POST' and 'susScheme' in request.form):
                scheme_id = request.form['scheme_id']
                self._scheme_handler.suspend_scheme(scheme_id)
        elif(request.method == 'POST' and 'delScheme' in request.form):
                scheme_id = request.form['scheme_id']       
                self._scheme_handler.delete_scheme(scheme_id)
        
        schemes = self._scheme_handler.get_all_scheme_data()
        return render_template('system_admin/dashboard.html', title='System Admin', schemes=schemes)

    @system_admin_login_required()    
    def system_new_scheme(self, request):
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
                        if self._scheme_handler.create_new_scheme(new_scheme_name):
                            scheme_admin_k_number = new_scheme_form.k_number.data
                            scheme_id = self._scheme_handler.get_scheme_id(new_scheme_name) ## new_scheme_name) ## return from create_new_scheme isntead?
                            ##
                            ## ToDo - below
                            ## 
                            password = "password"  ##urandom(16) ## send in email + force to change
                            hashed_password = generate_password_hash(password)
                            if self._student_handler.insert_student(scheme_id, scheme_admin_k_number, 'admin change', 'admin change', 'admin change', 2, 'admin change', 1, hashed_password, 1, 1): ## check res?
                                if self._scheme_handler.create_allocation_config_entry(scheme_id):
                                    flash("Scheme And Admin Account Succesfully Created")
                                else:
                                    flash("Scheme And Admin Account Created But Failed To Create Allocation Config")
                                    
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
        
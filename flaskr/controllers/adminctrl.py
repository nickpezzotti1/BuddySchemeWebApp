from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
import logging
from logic.adminlgc import AdminLogic

admin_blueprint = Blueprint('admin', __name__)
handler = AdminLogic()


@admin_blueprint.route('/admin')
def admin_dashboard():
    return handler.admin_dashboard()

@admin_blueprint.route('/admin/view_students', methods=['POST', 'GET'])
def admin_view_students():
    return handler.admin_view_students()

@admin_blueprint.route('/admin/student_details', methods=['GET', 'POST'])
def view_student_details():
    return handler.view_student_details()

@admin_blueprint.route('/admin/delete_student', methods=['POST'])
def delete_student_details():
    return handler.delete_student_details()

@admin_blueprint.route('/admin/general_settings')
def general_settings():

    return render_template('admin/general_settings.html', title='General Settings')

@admin_blueprint.route('/admin/allocation_algorithm')
def allocation_algorithm():
    return handler.allocation_algorithm()

@admin_blueprint.route('/admin/signup_settings')
def sign_up_settings():
    return render_template('admin/dashboard.html', title='Sign-Up Settings')

@admin_blueprint.route('/admin/allocate')
def allocate():
    return handler.allocate()

@admin_blueprint.route('/admin/manually_assign', methods=['GET', 'POST'])
def manually_assign():
    return handler.manually_assign()

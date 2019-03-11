from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import admin_login_required
import logging
from logic.adminlgc import AdminLogic

admin_blueprint = Blueprint('admin', __name__)
handler = AdminLogic()


@admin_blueprint.route('/admin')
# @admin_login_required()
def admin_dashboard():
    return handler.admin_dashboard()

@admin_blueprint.route('/admin/view_students', methods=['POST', 'GET'])
@admin_login_required()
def admin_view_students():
    return handler.admin_view_students()

@admin_blueprint.route('/admin/student_details', methods=['GET', 'POST'])
@admin_login_required()
def view_student_details():
    return handler.view_student_details()

@admin_blueprint.route('/admin/delete_student', methods=['POST'])
@admin_login_required()
def delete_student_details():
    return handler.delete_student_details()

@admin_blueprint.route('/admin/general_settings', methods=['GET', 'POST'])
# @admin_login_required()
def general_settings():
    return handler.general_settings()

@admin_blueprint.route('/admin/allocation_config', methods=['GET', 'POST'])
@admin_login_required()
def allocation_config():
    return handler.allocation_config()

@admin_blueprint.route('/admin/allocation_algorithm')
@admin_login_required()
def allocation_algorithm():
    return handler.allocation_algorithm()

@admin_blueprint.route('/admin/signup_settings')
@admin_login_required()
def sign_up_settings():
    return render_template('admin/dashboard.html', title='Sign-Up Settings')

@admin_blueprint.route('/admin/allocate')
@admin_login_required()
def allocate():
    return handler.allocate()

@admin_blueprint.route('/admin/manually_assign', methods=['GET', 'POST'])
@admin_login_required()
def manually_assign():
    return handler.manually_assign()

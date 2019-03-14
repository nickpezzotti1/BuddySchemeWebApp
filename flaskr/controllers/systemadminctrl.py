from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import system_admin_login_required
import logging
from logic.systemadminlgc import SystemAdminLogic

system_admin_blueprint = Blueprint('systemadmin', __name__)
handler = SystemAdminLogic()

@system_admin_blueprint.route('/system/', methods=['get', 'post'])
def system_admin_login():
    return handler.system_admin_login(request)

@system_admin_blueprint.route('/system/admin', methods=['get', 'post'])
@system_admin_login_required()
def system_admin_dashboard():
    return handler.system_admin_dashboard()

@system_admin_blueprint.route('/system/admin/new_scheme', methods=['get', 'post'])
@system_admin_login_required()
def system_new_scheme():
    return handler.system_new_scheme(request)

@system_admin_blueprint.route('/system/admin/view_scheme', methods=['post'])
@system_admin_login_required()
def system_view_scheme_dashboard():
    return handler.system_view_scheme_dashboard(request)


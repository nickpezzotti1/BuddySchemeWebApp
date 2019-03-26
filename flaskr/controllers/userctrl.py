from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
import logging
from logic.userlgc import UserLogic

user_blueprint = Blueprint('user', __name__)

handler = UserLogic()

@user_blueprint.route("/user")
#@permissioned_login_required(role="USER", redirect_on_fail="/dashboard")
def user():
    return handler.user()

@user_blueprint.route("/user/preferences", methods=['POST', 'GET'])
def user_preferences():
    return handler.user_preferences(request)

@user_blueprint.route('/user/buddy-list')
def user_buddy_list():
    return handler.user_buddy_list(request)

@user_blueprint.route("/user/delete", methods=['POST', 'GET'])
def user_delete():
    
    return handler.user_delete(request)

@user_blueprint.route('/user/buddy/<k_number_buddy>')
def user_buddy(k_number_buddy):
    return handler.user_buddy_view(k_number_buddy)

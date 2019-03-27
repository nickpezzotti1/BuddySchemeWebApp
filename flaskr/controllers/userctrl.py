from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flaskr.permissions import permissioned_login_required
import logging
from flaskr.logic.userlgc import UserLogic

user_blueprint = Blueprint('user', __name__)

handler = UserLogic()

@user_blueprint.route("/user")
@login_required
def user():
    return handler.user()


@user_blueprint.route("/user/preferences", methods=['POST', 'GET'])
@login_required
def user_preferences():
    return handler.user_preferences(request)


@user_blueprint.route('/user/buddy-list')
@login_required
def user_buddy_list():
    return handler.user_buddy_list(request)


@user_blueprint.route("/user/delete", methods=['POST', 'GET'])
@login_required
def user_delete():
    return handler.user_delete(request)


@user_blueprint.route("/user/reset-password", methods=['POST', 'GET'])
@login_required
def user_password_reset():
    return handler.user_password_reset(request)


@user_blueprint.route('/user/buddy/<k_number_buddy>')
@login_required
def user_buddy(k_number_buddy):
    return handler.user_buddy_view(k_number_buddy)

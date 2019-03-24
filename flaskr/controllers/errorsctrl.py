from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flaskr.logic.errorslgc import ErrorLogic


errors_blueprint = Blueprint('errors', __name__)
handler = ErrorLogic()


@errors_blueprint.app_errorhandler(404)
def error_404(error):
    return handler.error_404()


@errors_blueprint.app_errorhandler(403)
def error_403(error):
    return handler.error_403()


@errors_blueprint.app_errorhandler(500)
def error_500(error):
    return handler.error_500()


@errors_blueprint.app_errorhandler(503)
def error_503(error):
    return handler.error_503()


@errors_blueprint.app_errorhandler(504)
def error_504(error):
    return handler.error_504()

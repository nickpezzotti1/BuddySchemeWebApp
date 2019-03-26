import logging

from flask import Flask, redirect, render_template
from flask_login import LoginManager, current_user, login_required

import flaskr.controllers.adminctrl
import flaskr.controllers.errorsctrl
import flaskr.controllers.loginctrl
import flaskr.controllers.menteectrl
import flaskr.controllers.mentorctrl
from flaskr.config import Config
from flaskr.controllers import systemadminctrl
from flaskr.user import User

login_manager = LoginManager()
login_manager.login_view = "login.login"


@login_manager.user_loader
def load_user(id):
    return User.get(id)


log = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    login_manager.init_app(app)

    app.config.from_object(config_class)

    import flaskr.controllers
    app.register_blueprint(controllers.systemadminctrl.system_admin_blueprint)
    app.register_blueprint(controllers.adminctrl.admin_blueprint)
    app.register_blueprint(controllers.loginctrl.login_blueprint)
    app.register_blueprint(controllers.menteectrl.mentee_blueprint)
    app.register_blueprint(controllers.errorsctrl.errors_blueprint)
    app.register_blueprint(controllers.mentorctrl.mentor_blueprint)

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("index.html")

    @app.route("/terms-conditions")
    def terms_condititons():
        return render_template("terms_conditions.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        # if he is a mentor redirect to mentor
        # else if he is a mentee redirect to mentee
        # else {admin} redirect to admin page
        priv = current_user.priv
        if priv == 'system_admin':
            return redirect('/system/admin')
        elif priv == 'admin':
            return redirect('/admin')
        else:
            role = current_user.role
            if role == 'mentee':
                return redirect('/mentee')
            elif role == 'mentor':
                return redirect('/mentor')

        return redirect('/')

    return app

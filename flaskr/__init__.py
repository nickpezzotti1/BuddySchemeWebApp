from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha3_256
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging
from flask import Flask, flash, redirect, render_template, request, url_for
from flaskr.controllers import systemadminctrl
import flaskr.controllers.adminctrl as adminctrl
import flaskr.controllers.loginctrl as loginctrl
import flaskr.controllers.mentorctrl as mentorctrl
import flaskr.controllers.menteectrl as menteectrl
import flaskr.controllers.errorsctrl as errorsctrl

login_manager = LoginManager()
login_manager.login_view = "login.login"

log = logging.getLogger(__name__)

def create_app(config_class=None):
    app = Flask(__name__)
    login_manager.init_app(app)

    app.config['SECRET_KEY'] = 'powerful secretkey'
    app.config["EMAIL_CONFIRMATION_EXPIRATION"] = 86400
    app.config["PASSWORD_RESET_EXPIRATION"] = 86400
    app.config["MESSAGE_SEPARATION_TOKEN"] = "[" + sha3_256(bytes(app.config["SECRET_KEY"], "utf-8")).hexdigest() + "]"
    #app.config.from_object(Config)

    import flaskr.controllers
    app.register_blueprint(controllers.systemadminctrl.system_admin_blueprint)
    app.register_blueprint(controllers.adminctrl.admin_blueprint)
    app.register_blueprint(controllers.loginctrl.login_blueprint)
    app.register_blueprint(controllers.menteectrl.mentee_blueprint)
    app.register_blueprint(controllers.errorsctrl.errors_blueprint)
    app.register_blueprint(controllers.mentorctrl.mentor_blueprint)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id)

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

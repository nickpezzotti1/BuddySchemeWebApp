from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
from hashlib import sha3_256
from user import User
import controllers.systemadminctrl as systemadminctrl
import controllers.adminctrl as adminctrl
import controllers.loginctrl as loginctrl
import controllers.mentorctrl as mentorctrl
import controllers.menteectrl as menteectrl
import controllers.errorsctrl as errorsctrl
import logging



app = Flask(__name__)
app.config["SECRET_KEY"] = "powerful secretkey"
# app.config["SECURITY_PASSWORD_SALT"]=53
app.config["EMAIL_CONFIRMATION_EXPIRATION"] = 86400
app.config["PASSWORD_RESET_EXPIRATION"] = 86400
# Hash of secret key as token to make collision probability neglibible
app.config["MESSAGE_SEPARATION_TOKEN"] = "[" + sha3_256(bytes(app.config["SECRET_KEY"], "utf-8")).hexdigest() + "]"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"

app.register_blueprint(systemadminctrl.system_admin_blueprint)
app.register_blueprint(adminctrl.admin_blueprint)
app.register_blueprint(loginctrl.login_blueprint)
app.register_blueprint(menteectrl.mentee_blueprint)
app.register_blueprint(errorsctrl.errors_blueprint)
app.register_blueprint(mentorctrl.mentor_blueprint)


log = logging.getLogger(__name__)


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

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)

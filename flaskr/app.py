from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from forms import LoginForm, RegistrationForm
from flask_wtf import FlaskForm
from user import User
import basic as db
from permissions import permissioned_login_required
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config["SECRET_KEY"]="powerful secretkey"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    user = User(id)
    return user


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():    
    login_form = LoginForm(request.form)

    if login_form.login_submit.data: # if the login form was submitted
        if login_form.validate_on_submit(): # if the form was valid
            user = User(login_form.k_number.data)

            # if user exists in db then a password hash was successfully retrieved
            if(user.password):
                # check if he is authorised
                if check_password_hash(user.password, login_form.password.data):
                    # redirect to profile page, where he must insert his preferences
                    login_user(user, remember=False)
                    app.logger.warning('logged in')
                    return redirect("/dashboard")
                else:
                    app.logger.warning('wrong password')
                    return redirect("/login")
            else:
                return redirect("/login")
        else: # if the form was NOT valid
            # Flash the error message
            app.logger.warning('error logging in')
            return render_template("login.html", login_form=login_form)

    return render_template("login.html", login_form=login_form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    registration_form = RegistrationForm(request.form)

    if registration_form.registration_submit.data: # if the registation form was submitted
        if registration_form.validate_on_submit(): # if the form was valid
            # hash the user password
            first_name = registration_form.first_name.data
            last_name = registration_form.last_name.data
            k_number = registration_form.k_number.data
            # hashed_password = generate_password_hash(registration_form.password.data)
            hashed_password = generate_password_hash("12345678", method="sha256")

            db_insert_success = db.insert_student(k_number, first_name, last_name, "na", 2018, "na", hashed_password)
            app.logger.warning('register user: ' + str(db_insert_success))

            #redirect to profile page, where he must insert his preferences
            return redirect("/dashboard")
        else: # if the form was NOT valid
            # Flash the error message
            app.logger.warning('error registering')
            return render_template("signup.html", registration_form=registration_form)
    
    return render_template("signup.html", registration_form=registration_form)


@app.route("/dashboard")
@login_required
def dashboard():
    return current_user.k_number


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")


@app.route("/mentee/<k_number>")
@permissioned_login_required(role="MENTOR", redirect_on_fail="/dashboard")
def mentee(k_number):
    # ensure user is authenticated: the session is valid; the user is k_number

    # user_info = getMenteeData(k_number): Dictionary
            # Query database with k number to get the following fields:
                # k number: string
                # First Name: string
                # Last Name: string
                # Age: int
                # Hobbies: List[string]
                # Academic interests: List[string]
            # Format into dictionary
    user_info = {
        "k_number": "k1763763",
        "first_name": "Nicholas",
        "last_name": "Pezzotti",
        "age": 20,
        "hobbies": ["football", "poker"],
        "academic_interests": ["AI", "Blockchain"]
    }

    return render_template("user_screens/mentee_page.html", title="Your Profile", user_info=user_info)

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True, port=5000)

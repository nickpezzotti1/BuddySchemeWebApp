from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from forms import LoginForm, RegistrationForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"]="powerful secretkey"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    registration_form = RegistrationForm()
    if request.method == "POST" and registration_form.is_submitted():
        # add user to system
        return redirect(url_for("home"))

    login_form = LoginForm()
    if request.method == "POST" and login_form.is_submitted():
        # check if he is authorised
        return redirect(url_for("home"))

    return render_template("login.html", registration_form=registration_form, login_form=login_form)


@app.route("/mentee/<k_number>")
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

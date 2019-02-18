from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from forms import LoginForm, RegistrationForm
from flask_wtf import FlaskForm
from user import User
import basic as db
from permissions import permissioned_login_required
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json

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
            is_mentor = registration_form.is_mentor.data
            # hashed_password = generate_password_hash(registration_form.password.data)
            hashed_password = generate_password_hash("12345678", method="sha256")

            db_insert_success = db.insert_student(k_number, first_name, last_name, "na", 2018, "na", (1 if is_mentor else 0), hashed_password, False)
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
    # if he is a mentor redirect to mentor
    # else if he is a mentee redirect to mentee
    # else {admin} redirect to admin page
    return redirect("/mentee")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")

@app.route("/mentor")
#@permissioned_login_required(role="MENTOR", redirect_on_fail="/dashboard")
def mentor():

    user_info = get_all_user_info(current_user.k_number)

    return render_template("user_screens/mentor/mentor_dashboard_page.html", title="Your Profile", user_info=user_info)

@app.route("/mentee")
#@permissioned_login_required(role="MENTEE", redirect_on_fail="/dashboard")
def mentee():
    
    user_info = get_all_user_info(current_user.k_number)

    return render_template("user_screens/mentee/mentee_dashboard_page.html", title="Your Profile", user_info=user_info)

@app.route("/mentor/preferences", methods = ['POST', 'GET'])
def mentor_preferences():

    if request.method == "POST":
        # TODO: Perform validation before updating table
        # user_info['hobbies'] = request.form.getlist('hobbies')
        # user_info['interests'] = request.form.getlist('interests')
        # print(request.form.getlist('hobbies'))
        #### db.update_informations(current_user.k_number, hobbies=request.form.getlist('hobbies')[0], interests=request.form.getlist('interests')[0])
        return redirect(url_for("mentor"))
    else:
        user_info = dict(db.get_user_data(current_user.k_number), **db.get_user_data(current_user.k_number))
        return render_template("user_screens/mentor/mentor_preferences_page.html", title="Your Preferences", user_info=user_info)

@app.route("/mentee/preferences", methods = ['POST', 'GET'])
def mentee_preferences():
    if request.method == "POST":
        # TODO: Perform validation before updating table
        # mentee_user_info['hobbies'] = request.form.getlist('hobbies')
        # mentee_user_info['interests'] = request.form.getlist('interests')
        # print(request.form.getlist('hobbies'))
        #### db.update_informations(current_user.k_number, hobbies=request.form.getlist('hobbies')[0], interests=request.form.getlist('interests')[0])
        return redirect(url_for("mentee"))
    else:
        user_info = dict(db.get_user_data(current_user.k_number), **db.get_user_data(current_user.k_number))
        return render_template("user_screens/mentee/mentee_preferences_page.html", title="Your Preferences", user_info=user_info)

@app.route('/mentor/mentee-list')
def mentor_mentee_list():
    mentee_list = db.get_mentees(current_user.k_number)

    # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
    mentee_list_data = {}

    # Format results into nested dict for use on page
    for mentee in mentee_list:
        mentee_k_number = mentee['mentee_k_number']
        mentee_list_data[mentee_k_number] = db.get_user_data(mentee_k_number)

    return render_template("user_screens/mentor/mentor_mentee_list_page.html", title="Your Mentees", mentees=mentee_list_data)

@app.route('/mentee/mentor-list')
def mentee_mentor_list():
    mentor_list = db.get_mentors(current_user.k_number)

    # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
    mentor_list_data = {}

    # Format results into nested dict for use on page
    for mentor in mentor_list:
        mentor_k_number = mentor['mentor_k_number']
        mentor_list_data[mentor_k_number] = db.get_user_data(mentor_k_number)

    return render_template("user_screens/mentee/mentee_mentor_list_page.html", title="Your Mentors", mentors=mentor_list_data)

@app.route('/mentor/mentee/<k_number_mentee>')
def mentor_mentee(k_number_mentee):
    return render_template("user_screens/mentor/mentor_mentee_page.html", title="Your Mentee", mentee_info=db.get_user_data(k_number_mentee), k_number_mentee=k_number_mentee)

@app.route('/mentee/mentor/<k_number_mentor>')
def mentee_mentor(k_number_mentor):

    return render_template('user_screens/mentee_mentor_page.html', title='Your Mentor', mentor_info=mentors[k_number_mentor], k_number_mentor=k_number_mentor)


@app.route('/admin')
def admin_dashboard():

    return render_template('admin/dashboard.html', title='Admin Dashboard')

@app.route('/admin/view_students', methods=['POST', 'GET'])
def admin_view_students():
    data = db.get_all_students_data_basic()
    return render_template('admin/view_students.html', title='View Students', data=data)

@app.route('/admin/student_details', methods=['POST'])
def view_student_details():
    if(request.method == 'POST'):
        kNum = request.form['knum']
        udata = db.get_user_data(kNum)
        info = db.get_information(kNum)
        isTor = True #udata.is_mentor change
        if isTor:
            matches = db.get_mentee_details(kNum)
        else:
            matches = db.get_mentor_details(kNum)

        return render_template('admin/student_details.html', title='Details For ' + kNum, udata=udata, info=info, matches=matches)
    else:
        admin_view_students()

@app.route('/admin/general_settings')
def general_settings():

    return render_template('admin/general_settings.html', title='General Settings')

@app.route('/admin/matching_settings')
def matching_settings():
    return render_template('admin/matching_settings.html', title='Matching Settings') # change

@app.route('/admin/signup_settings')
def sign_up_settings():
    return render_template('admin/dashboard.html', title='Sign-Up Settings')

@app.route('/admin/allocate')
def allocate():
    # Replace template_input with real input from db

    # Get all mentors from database
    mentors = db.get_all_mentors()

    # Get all mentees from database
    mentees = db.get_all_mentees()
    print(mentees)

    input = {"mentors" : [], "mentees": []}
    for mentor in mentors :
        input["mentors"].append(
        {
            "ID": int(mentor["mentor_k_number"][1:]), #TODO
            "age": 20,
            "isMale": True,
            "menteeLimit": 1
        }
        )

    for mentee in mentees :
        input["mentees"].append(
        {
            "ID": int(mentee["mentee_k_number"][1:]), #TODO
            "age": 20,
            "isMale": True
        }
        )

    input_string = json.dumps(input)

    response = requests.post('https://c4t2nyi7y4.execute-api.us-east-2.amazonaws.com/default', data = input_string)
    # remove surrounding quotes (first and last char) and remove the backslashes (ASK NICHOLAS, problem with aws formatting)
    response_text = response.text[1:-1].replace("\\", "")
    json_response = json.loads(response_text)
    pairs = json_response["assignments"]

    try:
        for pair in pairs:
            db.insert_mentor_mentee("k"+pair["mentor_id"], "k"+pair["mentee_id"])
    except:
        print("Error in inserting into db")

    ## update the database with the new assignments

    return "Entered the following allocations in the database" + response_text


def get_all_user_info(k_number):
    """ Get all user info from database and format into a single dict"""
    
    user_info = db.get_user_data(k_number)
    
    # retrieve interests from db and format into a list
    interests = []
    for interest_pair in db.get_interests(k_number):
        interests.append(interest_pair["interest"])

    user_info["interests"] = interests

    # retrieve hobbies from db and format into a list
    hobbies = []
    for hobby_pair in db.get_hobbies(k_number):
        hobbies.append(hobby_pair["hobby"])

    user_info["hobbies"] = hobbies

    return user_info

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)

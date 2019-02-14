import basic
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

app = Flask(__name__)

# Mock data

user_info = {
    "k_number": "k1764064",
    "k_number_mentee": "k1738383",
    "first_name": "Nicholas",
    "last_name": "Pezzotti",
    "age": 20,
    "hobbies": ["Football", "Poker"],
    "academic_interests": ["AI", "Blockchain"]
}
mentee_user_info = {
    "k_number": "k1764064",
    "k_number_mentee": "k1738383",
    "first_name": "Nihad",
    "last_name": "Rahman",
    "age": 20,
    "hobbies": ["Football", "Poker"],
    "academic_interests": ["AI", "Blockchain"]
}

mentees = {
    "k1803945": {
        "first_name": "Alice",
        "last_name": "Apple",
        "age": 21,
    },
    "k1874859": {
        "first_name": "Bob",
        "last_name": "Banana",
        "age": 22,
    },
    "k1673459": {
        "first_name": "Charlie",
        "last_name": "Carrot",
        "age": 19,
    }
}

mentors = {
    "k1803945": {
        "first_name": "Jardin",
        "last_name": "Apple",
        "age": 21,
    },
    "k1874859": {
        "first_name": "Nick",
        "last_name": "Banana",
        "age": 22,
    },
    "k1673459": {
        "first_name": "Charlie",
        "last_name": "Carrot",
        "age": 19,
    }
}

@app.route("/")
@app.route("/home")
def hello():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/mentor")
def mentor():
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

    return render_template("user_screens/mentor_dashboard_page.html", title="Your Profile", user_info=user_info)

@app.route("/mentee")
def mentee():

    return render_template("user_screens/mentee_dashboard_page.html", title="Your Profile", user_info=mentee_user_info)

@app.route("/mentor/preferences", methods=['POST', 'GET'])
def mentor_preferences():

    if request.method == "POST":
        user_info['hobbies'] = request.form.getlist('hobbies')
        user_info['academic_interests'] = request.form.getlist('academic_interests')
        
        return redirect(url_for("mentor"))
    else:
        return render_template("user_screens/mentor_preferences_page.html", title="Your Preferences", user_info=user_info)

@app.route("/mentee/preferences", methods=['POST', 'GET'])
def mentee_preferences():

    if request.method == "POST":
        mentee_user_info['hobbies'] = request.form.getlist('hobbies')
        mentee_user_info['academic_interests'] = request.form.getlist('academic_interests')
        
        return redirect(url_for("mentee"))
    else:
        return render_template("user_screens/mentee_preferences_page.html", title="Your Preferences", user_info=mentee_user_info)


@app.route("/mentor/mentee-list")
def mentor_mentee_list():

    # query database for all mentees the mentor has

    return render_template("user_screens/mentor_mentee_list_page.html", title="Your Mentees", user_info=user_info, mentees=mentees)

@app.route("/mentee/mentor-list")
def mentee_mentor_list():

    # query database for all mentees the mentor has

    return render_template("user_screens/mentee_mentor_list_page.html", title="Your Mentors", user_info=mentee_user_info, mentors=mentors)

@app.route("/mentor/mentee/<k_number_mentee>")
def mentor_mentee(k_number_mentee):

    return render_template("user_screens/mentor_mentee_page.html", title="Your Mentee", mentee_info=mentees[k_number_mentee], k_number_mentee=k_number_mentee)

@app.route("/mentee/mentor/<k_number_mentor>")
def mentee_mentor(k_number_mentor):

    return render_template("user_screens/mentee_mentor_page.html", title="Your Mentor", mentor_info=mentors[k_number_mentor], k_number_mentor=k_number_mentor)


@app.route("/admin")
def admin_dashboard():
    
    return render_template("admin/dashboard.html", title="Admin Dashboard")

@app.route("/admin/view_students", methods=['POST', 'GET'])
def admin_view_students():
    data = basic.get_all_students_data_basic()
    return render_template("admin/view_students.html", title="View Students", data=data)

@app.route("/admin/student_details", methods=['POST'])
def view_student_details():
    if(request.method == 'POST'):
        kNum = request.form["knum"]
        udata = basic.get_user_data(kNum)
        info = basic.get_information(kNum)
        isTor = True #udata.is_mentor change
        if isTor:
            matches = basic.get_mentee_details(kNum)
        else:
            matches = basic.get_mentor_details(kNum)
                 
        return render_template("admin/student_details.html", title="Details For " + kNum, udata=udata, info=info, matches=matches)
    else:
        admin_view_students()
    
@app.route("/admin/general_settings")
def general_settings():
    
    return render_template("admin/general_settings.html", title="General Settings")
    
@app.route("/admin/matching_settings")
def matching_settings():
    
    return render_template("admin/matching_settings.html", title="Matching Settings") # change
@app.route("/admin/signup_settings")
def sign_up_settings():

    
    return render_template("admin/dashboard.html", title="Sign-Up Settings")

# We only need this for local dev
if __name__ == '__main__':
    app.run(debug=True)
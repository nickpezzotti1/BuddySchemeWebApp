import basic as db
import basic as db
from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from forms import LoginForm, RegistrationForm
import json
from permissions import permissioned_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from auth_token import verify_token
import requests
from user import User
from werkzeug.security import check_password_hash, generate_password_hash
from emailer import send_email, send_email_confirmation_to_user

admin_blueprint = Blueprint('admin', __name__)




@admin_blueprint.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@admin_blueprint.route('/admin/view_students', methods=['POST', 'GET'])
def admin_view_students():
    data = db.get_all_students_data_basic()
    return render_template('admin/view_students.html', title='View Students', data=data)

@admin_blueprint.route('/admin/student_details', methods=['GET', 'POST'])
def view_student_details():
    if(request.method == 'POST' and 'knum' in request.form):
        kNum = request.form['knum']
        if('mkAdmin' in request.form):
            res = db.alter_admin_status(kNum, True)
        elif('rmAdmin' in request.form):
            res = db.alter_admin_status(kNum, False)
        elif('mkAlloc' in request.form):
            torNum = request.form['torNum']
            teeNum = request.form['teeNum']
            res = db.make_manual_allocation(teeNum, torNum)
        elif("rmAlloc" in request.form):
            torNum = request.form['torNum']
            teeNum = request.form['teeNum']
            res = db.remove_allocation(teeNum, torNum)
        udata = db.get_user_data(kNum)
        hobbies = db.get_hobbies(kNum)
        interests = db.get_interests(kNum)
        isTor = udata['is_mentor']
        if isTor:
            matches = db.get_mentee_details(kNum)
        else:
            matches = db.get_mentor_details(kNum)
        return render_template('admin/student_details.html', title='Details For ' + kNum, udata=udata, hobbies=hobbies, interests=interests, matches=matches)
    else:
        return redirect(url_for('admin.admin_view_students'))

@admin_blueprint.route('/admin/delete_student', methods=['POST'])
def delete_student_details():
    if(request.method == 'POST' and 'knum' in request.form):
        kNum = request.form['knum']
        res = db.delete_students(kNum)
        return render_template('admin/delete_student.html', title='Delete Student Profile ' + kNum, res=res, k_number=kNum)
    else:
        return redirect(url_for('admin.admin_view_students'))

@admin_blueprint.route('/admin/general_settings')
def general_settings():

    return render_template('admin/general_settings.html', title='General Settings')

@admin_blueprint.route('/admin/allocation_algorithm')
def allocation_algorithm():
    return render_template('admin/allocation_algorithm.html', title='allocation_algorithm', assignments=allocate())

@admin_blueprint.route('/admin/signup_settings')
def sign_up_settings():
    return render_template('admin/dashboard.html', title='Sign-Up Settings')

@admin_blueprint.route('/admin/allocate')
def allocate():
    input_string = generate_mentee_and_mentor_json()

    response = requests.post('https://c4t2nyi7y4.execute-api.us-east-2.amazonaws.com/default', data=input_string)
    # remove surrounding quotes (first and last char) and remove the backslashes (ASK NICHOLAS, problem with aws formatting)
    response_text = response.text[1:-1].replace("\\", "")
    json_response = json.loads(response_text)
    pairs = json_response["assignments"]

    try:
        for pair in pairs:
            db.insert_mentor_mentee("k" + pair["mentor_id"], "k" + pair["mentee_id"])
    except:
        print("Error in inserting into db")

    return "The following assignments have been made:" + str(json_response["assignments"])

def generate_mentee_and_mentor_json():
    # Get all mentors from database
    mentors = db.get_all_mentors()

    # Get all mentees from database
    mentees = db.get_all_mentees()

    input = {"mentors": [], "mentees": []}
    for mentor in mentors:
        input["mentors"].append(
                                {
                                    "ID": int(mentor["mentor_k_number"][1:]), #TODO
                                    "age": 20,
                                    "isMale": True,
                                    "menteeLimit": 1
                                }
                            )

    for mentee in mentees:
        input["mentees"].append(
                                {
                                    "ID": int(mentee["mentee_k_number"][1:]), #TODO
                                    "age": 20,
                                    "isMale": True
                                }
                            )

    return json.dumps(input)

@admin_blueprint.route('/admin/manually_assign', methods=['GET', 'POST'])
def manually_assign():
    if(request.method == 'POST'):
        kNum = request.form['knum']
        udata = db.get_user_data(kNum)
        potentials = db.get_manual_allocation_matches(kNum, udata['is_mentor'])
        return render_template('admin/manually_assign.html', title='Manually Assign Match', udata=udata, potentials=potentials) # imprv title?
    else:
        return redirect(url_for('admin.admin_view_students'))
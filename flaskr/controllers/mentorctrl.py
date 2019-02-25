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
import controllers.adminctrl as adminctrl
import logging

mentor_blueprint = Blueprint('mentor', __name__)


@mentor_blueprint.route("/mentor")
#@permissioned_login_required(role="MENTOR", redirect_on_fail="/dashboard")
def mentor():

    user_info = get_all_user_info(current_user.k_number)

    return render_template("user_screens/mentor/mentor_dashboard_page.html", title="Your Profile", user_info=user_info)

@mentor_blueprint.route("/mentor/preferences", methods=['POST', 'GET'])
def mentor_preferences():

    if request.method == "POST":
        update_user_preferences(current_user.k_number, request.form.getlist('hobbies'), request.form.getlist('interests'))
        return redirect(url_for("mentor"))
    else:
        user_info = get_all_user_info(current_user.k_number)
        return render_template("user_screens/mentor/mentor_preferences_page.html", title="Your Preferences", user_info=user_info)

@mentor_blueprint.route('/mentor/mentee-list')
def mentor_mentee_list():
    mentee_list = db.get_mentees(current_user.k_number)

    # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
    mentee_list_data = {}

    # Format results into nested dict for use on page
    for mentee in mentee_list:
        mentee_k_number = mentee['mentee_k_number']
        mentee_list_data[mentee_k_number] = db.get_user_data(mentee_k_number)

    return render_template("user_screens/mentor/mentor_mentee_list_page.html", title="Your Mentees", mentees=mentee_list_data)

@mentor_blueprint.route('/mentor/mentee/<k_number_mentee>')
def mentor_mentee(k_number_mentee):
    return render_template("user_screens/mentor/mentor_mentee_page.html", title="Your Mentee", mentee_info=db.get_user_data(k_number_mentee), k_number_mentee=k_number_mentee)

@mentor_blueprint.route('/mentee/mentor/<k_number_mentor>')
def mentee_mentor(k_number_mentor):

    return render_template('user_screens/mentee_mentor_page.html', title='Your Mentor', mentor_info=mentors[k_number_mentor], k_number_mentor=k_number_mentor)



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

def update_user_preferences(k_number, hobbies, interests):
    # delete all hobbies and interests
    db.delete_hobbies(k_number)
    db.delete_interests(k_number)

    # insert hobbies and interests according to those ticked
    for hobby in hobbies:
        db.insert_hobby(k_number, hobby)

    for interest in interests:
        db.insert_interest(k_number, interest)
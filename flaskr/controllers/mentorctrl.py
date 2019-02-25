from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from permissions import permissioned_login_required
import logging
from logic.mentorlgc import MentorLogic

mentor_blueprint = Blueprint('mentor', __name__)

handler = MentorLogic()

@mentor_blueprint.route("/mentor")
#@permissioned_login_required(role="MENTOR", redirect_on_fail="/dashboard")
def mentor():

    return handler.mentor()

@mentor_blueprint.route("/mentor/preferences", methods=['POST', 'GET'])
def mentor_preferences():

    return handler.mentor_preferences(request)

@mentor_blueprint.route('/mentor/mentee-list')
def mentor_mentee_list():
    
    return handler.mentor_mentee_list(request)

@mentor_blueprint.route('/mentor/mentee/<k_number_mentee>')
def mentor_mentee(k_number_mentee):
    return render_template("user_screens/mentor/mentor_mentee_page.html", title="Your Mentee", mentee_info=db.get_user_data(k_number_mentee), k_number_mentee=k_number_mentee)

@mentor_blueprint.route('/mentee/mentor/<k_number_mentor>')
def mentee_mentor(k_number_mentor):

    return render_template('user_screens/mentee_mentor_page.html', title='Your Mentor', mentor_info=mentors[k_number_mentor], k_number_mentor=k_number_mentor)

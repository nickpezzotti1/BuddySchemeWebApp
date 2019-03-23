from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from datetime import date
import logging
from models.allocationmdl import AllocationModel
from models.student_interestmdl import StudentInterestModel
from models.student_hobbymdl import StudentHobbyModel
from models.interestmdl import InterestModel
from models.hobbymdl import HobbyModel
from models.studentmdl import StudentModel

class MenteeLogic():

    def mentee(self):

        try:
            data_definitions = self.get_data_definitions()
            user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)

            return render_template("user_screens/mentee/mentee_dashboard_page.html", title="Your Profile", user_data=user_data)

        except Exception as e:
                self._log.exception("Could not execute get mentee logic")
                return abort(500)


    def mentee_preferences(self, request):

        try:
            if request.method == "POST":
                self._student_hobby_handler.update_hobbies(current_user.scheme_id, current_user.k_number, request.form.getlist('hobby'))
                self._student_interest_handler.update_interests(current_user.scheme_id, current_user.k_number, request.form.getlist('interest'))
                self._student_handler.update_date_of_birth(current_user.scheme_id, current_user.k_number, request.form['date_of_birth'])
                self._student_handler.update_gender(current_user.scheme_id, current_user.k_number, request.form['gender'])
                return redirect(url_for("mentee.mentee"))
            else:
                data_definitions = self.get_data_definitions()
                user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)
                return render_template("user_screens/mentee/mentee_preferences_page.html", title="Your Preferences", user_data=user_data, data_definitions=data_definitions)

        except Exception as e:
                self._log.exception("Could not execute mentee preferences logic")
                return abort(500)

    def mentee_mentor_list(self, request):

        try:
            mentor_list = self._allocation_handler.get_mentors(current_user.scheme_id, current_user.k_number)

            # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
            mentor_list_data = {}

            # Format results into nested dict for use on page
            for mentor in mentor_list:
                mentor_k_number = mentor['mentor_k_number']
                mentor_list_data[mentor_k_number] = self._student_handler.get_user_data(current_user.scheme_id, mentor_k_number)

            return render_template("user_screens/mentee/mentee_mentor_list_page.html", title="Your Mentors", mentors=mentor_list_data)

        except Exception as e:
                self._log.exception("Could not execute mentee mentor list logic")
                return abort(500)

    def mentor_view(self, k_number_mentor):

        try:
            return render_template("user_screens/mentee/mentee_mentor_page.html", title="Your Mentor", mentor_data=self._student_handler.get_user_data(current_user.scheme_id, k_number_mentor), k_number_mentor=k_number_mentor)

        except Exception as e:
            self._log.exception("Could not execute mentor view logic")
            return abort(500)

    #### HELPER FUNCTIONS

    def get_data_definitions(self):
        """ Get a list of all possible hobbies and interests """
        try:
            data_definitions = {
                "hobbies": self._hobby_handler.get_hobby_list(),
                "interests": self._interest_handler.get_interest_list()
            }

            return data_definitions

        except Exception as e:
                self._log.exception("Could not execute mentor get preference list logic")
                return abort(500)

    def get_all_user_data(self, scheme_id, k_number):
        """ Get all user data from database and format into a single dict"""
        try:
            user_data = self._student_handler.get_user_data(scheme_id, k_number)

            # retrieve interests from db and format into a list
            interests = {}
            for interest in self._student_interest_handler.get_interests(scheme_id, k_number):
                interests[interest["interest_id"]] = interest["interest_name"]

            user_data["interests"] = interests

            # retrieve hobbies from db and format into a list
            hobbies = {}
            for hobby in self._student_hobby_handler.get_hobbies(scheme_id, k_number):
                hobbies[hobby["hobby_id"]] = hobby["hobby_name"]

            user_data["hobbies"] = hobbies

            return user_data

        except Exception as e:
                self._log.exception("Could not execute get all user data logic")
                return abort(500)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._allocation_handler = AllocationModel()
            self._student_handler = StudentModel()
            self._student_hobby_handler = StudentHobbyModel()
            self._student_interest_handler = StudentInterestModel()
            self._hobby_handler = HobbyModel()
            self._interest_handler = InterestModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(500)

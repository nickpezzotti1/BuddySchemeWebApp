from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging
from models.allocationmdl import AllocationModel
from models.interestmdl import InterestModel
from models.hobbiesmdl import HobbiesModel
from models.studentmdl import StudentModel


class MenteeLogic():

    def mentee(self):

        try:
            user_info = self.get_all_user_info(current_user.k_number)

            return render_template("user_screens/mentee/mentee_dashboard_page.html", title="Your Profile", user_info=user_info)

        except Exception as e:
                self._log.exception("Could not execute get mentee logic")
                return abort(404)


    def mentee_preferences(self,request):

        try:
            if request.method == "POST":
                self.update_user_preferences(current_user.k_number, request.form.getlist('hobbies'), request.form.getlist('interests'))
                return redirect(url_for("mentee.mentee"))
            else:
                user_info = self.get_all_user_info(current_user.k_number)
                return render_template("user_screens/mentee/mentee_preferences_page.html", title="Your Preferences", user_info=user_info)

        except Exception as e:
                self._log.exception("Could not execute mentee preferences logic")
                return abort(404)


    def mentee_mentor_list(self,request):

        try:
            mentor_list = self._allocation_handler.get_mentors(current_user.k_number)
            

            # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
            mentor_list_data = {}

            # Format results into nested dict for use on page
            for mentor in mentor_list:
                mentor_k_number = mentor['mentor_k_number']
                mentor_list_data[mentor_k_number] = self._student_handler.get_user_data(mentor_k_number)

            return render_template("user_screens/mentee/mentee_mentor_list_page.html", title="Your Mentors", mentors=mentor_list_data)

        except Exception as e:
                self._log.exception("Could not execute mentee mentor list logic")
                return abort(404)

    def mentor_view(self, k_number):
        try:
            mentor_info = self._student_handler.get_user_data(k_number)
            return render_template("user_screens/mentee/mentee_mentor_page.html", title="Your Mentor", mentor_info=mentor_info)

        except Exception as e:
                self._log.exception("Could not execute mentor view logic")
                return abort(404)

    def get_all_user_info(self,k_number):
        """ Get all user info from database and format into a single dict"""
        try:
            user_info = self._student_handler.get_user_data(k_number)

            # retrieve interests from db and format into a list
            interests = []
            for interest_pair in self._interest_handler.get_interests(k_number):
                interests.append(interest_pair["interest"])

            user_info["interests"] = interests

            # retrieve hobbies from db and format into a list
            hobbies = []
            for hobby_pair in self._hobbies_handler.get_hobbies(k_number):
                hobbies.append(hobby_pair["hobby"])

            user_info["hobbies"] = hobbies

            return user_info

        except Exception as e:
                self._log.exception("Could not execute get all user info logic")
                return abort(404)

    def update_user_preferences(self,k_number, hobbies, interests):
        # delete all hobbies and interests
        try:
            self._hobbies_handler.delete_hobbies(k_number)
            self._interest_handler.delete_interests(k_number)

            # insert hobbies and interests according to those ticked
            for hobby in hobbies:
                self._hobbies_handler.insert_hobby(k_number, hobby)

            for interest in interests:
                self._interest_handler.insert_interest(k_number, interest)

        except Exception as e:
                self._log.exception("Could not execute update user preferences logic")
                return abort(404)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._allocation_handler = AllocationModel()
            self._student_handler = StudentModel()
            self._hobbies_handler = HobbiesModel()
            self._interest_handler = InterestModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(404)

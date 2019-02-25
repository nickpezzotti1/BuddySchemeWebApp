import basic as db
from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging

class MentorLogic():


    def mentor(self):

        user_info = self.get_all_user_info(current_user.k_number)

        return render_template("user_screens/mentor/mentor_dashboard_page.html", title="Your Profile", user_info=user_info)


    def mentor_preferences(self,request):

        if request.method == "POST":
            self.update_user_preferences(current_user.k_number, request.form.getlist('hobbies'), request.form.getlist('interests'))
            return redirect(url_for("mentor"))
        else:
            user_info = self.get_all_user_info(current_user.k_number)
            return render_template("user_screens/mentor/mentor_preferences_page.html", title="Your Preferences", user_info=user_info)


    def mentor_mentee_list(self,request):
        mentee_list = db.get_mentees(current_user.k_number)

        # Object to hold all the mentees. This takes the form of a nested dictionary indexed by k_numbers
        mentee_list_data = {}

        # Format results into nested dict for use on page
        for mentee in mentee_list:
            mentee_k_number = mentee['mentee_k_number']
            mentee_list_data[mentee_k_number] = db.get_user_data(mentee_k_number)

        return render_template("user_screens/mentor/mentor_mentee_list_page.html", title="Your Mentees", mentees=mentee_list_data)



    def get_all_user_info(self,k_number):
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

    def update_user_preferences(self,k_number, hobbies, interests):
        # delete all hobbies and interests
        db.delete_hobbies(k_number)
        db.delete_interests(k_number)

        # insert hobbies and interests according to those ticked
        for hobby in hobbies:
            db.insert_hobby(k_number, hobby)

        for interest in interests:
            db.insert_interest(k_number, interest)

    def __init__(self):
            self._log = logging.getLogger(__name__)
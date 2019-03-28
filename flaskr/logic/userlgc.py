from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort, current_app
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from datetime import date
from flaskr.forms import UserPreferencesForm, ResetPasswordForm
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from flaskr.models.allocationmdl import AllocationModel
from flaskr.models.hobbymdl import HobbyModel
from flaskr.models.interestmdl import InterestModel
from flaskr.models.student_hobbymdl import StudentHobbyModel
from flaskr.models.student_interestmdl import StudentInterestModel
from flaskr.models.studentmdl import StudentModel
from flaskr.models.schememdl import SchemeModel
from flaskr.user import SystemAdmin

class UserLogic():

    def user(self):

        try:
            data_definitions = self.get_data_definitions(current_user.scheme_id)
            user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)

            return render_template("user/dashboard_page.html", title="Your Profile", user_data=user_data)

        except Exception as e:
                self._log.exception("Could not execute get user logic")
                return abort(500)

    def user_preferences(self, request):
        try:
            user_data = self.get_all_user_data(current_user.scheme_id, current_user.k_number)

            # Create new form and pre-populate with existing values
            form = UserPreferencesForm(request.form, date_of_birth=user_data["date_of_birth"], gender=user_data["gender"], buddy_limit=user_data["buddy_limit"], interests=user_data["interests"], hobbies=user_data["hobbies"])

            # Update data on form submission
            if request.method == "POST" :
                self._student_interest_handler.update_interests(current_user.scheme_id, current_user.k_number, form.interests.data)
                self._student_hobby_handler.update_hobbies(current_user.scheme_id, current_user.k_number, form.hobbies.data)
                self._student_handler.update_date_of_birth(current_user.scheme_id, current_user.k_number, form.date_of_birth.data)
                self._student_handler.update_gender(current_user.scheme_id, current_user.k_number, form.gender.data)

                # If mentor 
                if user_data["is_mentor"]:
                    buddy_limit = form.buddy_limit.data
                    system_buddy_limit = current_app.config["BUDDY_LIMIT"]

                    if buddy_limit > system_buddy_limit:
                        flash(f"System's buddy limit is {system_buddy_limit}.")
                        buddy_limit = system_buddy_limit

                    self._student_handler.update_buddy_limit(current_user.scheme_id, current_user.k_number, buddy_limit)
                else:
                    self._student_handler.update_buddy_limit(current_user.scheme_id, current_user.k_number)

                return redirect(url_for("user.user"))
            else:
                # Pre-populate interest and hobbies with existing values
                form.interests.data=[interest_id for interest_id, interest_name in user_data["interests"].items()]
                form.hobbies.data=[hobby_id for hobby_id, hobby_name in user_data["hobbies"].items()]

                # Populate possible choices using data from data_definitions
                data_definitions = self.get_data_definitions(current_user.scheme_id)
                gender_definitions = self.get_gender_definitions()

                form.gender.choices = [(gender_type, gender_type) for gender_type in gender_definitions]
                form.interests.choices = [(interest["id"], interest["interest_name"]) for interest in data_definitions["interests"]]
                form.hobbies.choices = [(hobby["id"], hobby["hobby_name"]) for hobby in data_definitions["hobbies"]]

                return render_template("user/preferences_page.html", title="Your Preferences", user_data=user_data, form=form)

        except Exception as e:
                self._log.exception("Could not execute user preferences logic")
                return abort(500)


    def user_delete(self, request):
        """ Will delete all the users informations from the database"""

        try:
            if request.method == "POST":
                flash("Be careful you are about to delete all of your data")
                self._student_handler.delete_students(current_user.scheme_id, current_user.k_number)
                return redirect(url_for("user.user"))
            else:
                return render_template("user/delete_page.html")

        except Exception as e:
            self._log.exception("Could not delete student")
            return abort(500)
    
    def user_password_reset(self, request):
        reset_password_form = ResetPasswordForm(request.form)

        if request.method == "POST":
            if reset_password_form.validate_on_submit():
                if check_password_hash(current_user.password, reset_password_form.old_password.data):
                    new_hashed_password = generate_password_hash(reset_password_form.password.data)

                    temp = current_user.get_id()
                    (role, email) = temp.split(":")

                    # if first element is `sysadmin` instead of a scheme_id
                    # call function to reset `sysadmin` pass
                    if role == "sysadmin":
                        self._scheme_handler.update_hash_password(email, new_hashed_password)
                    else:
                        # regular user reset
                        self._student_handler.update_hash_password(current_user.scheme_id, current_user.k_number, new_hashed_password)

                    flash("Password successfully updated")
                else:
                    flash("Old password incorrect")
            else:
                flash("Please double check your new password is valid.")
                
        return render_template("user/reset_password.html", reset_password_form=reset_password_form)

    def user_buddy_list(self,request):

        try:

            # Object to hold all the buddies. This takes the form of a nested dictionary indexed by k_numbers
            buddy_list_data = {}

            # Get all buddies depending on whether the user is a mentor or mentee
            user_is_mentor = self._student_handler.get_user_data(current_user.scheme_id, current_user.k_number)["is_mentor"]

            if user_is_mentor:
                buddy_list = self._allocation_handler.get_mentees(current_user.scheme_id, current_user.k_number)

                # Format results into nested dict for use on page
                for buddy in buddy_list:
                    buddy_k_number = buddy['mentee_k_number']
                    buddy_list_data[buddy_k_number] = self._student_handler.get_user_data(current_user.scheme_id, buddy_k_number)

            else:
                buddy_list = self._allocation_handler.get_mentors(current_user.scheme_id, current_user.k_number)

                # Format results into nested dict for use on page
                for buddy in buddy_list:
                    buddy_k_number = buddy['mentor_k_number']
                    buddy_list_data[buddy_k_number] = self._student_handler.get_user_data(current_user.scheme_id, buddy_k_number)

            return render_template("user/buddy_list_page.html", title="Your Buddies", buddies=buddy_list_data)

        except Exception as e:
                self._log.exception("Could not execute buddy list logic")
                return abort(500)

    def user_buddy_view(self, k_number_buddy):

        try:
            return render_template("user/buddy_page.html", title="Your Mentee", buddy_data=self._student_handler.get_user_data(current_user.scheme_id, k_number_buddy), k_number_buddy=k_number_buddy)

        except Exception as e:
            self._log.exception("Could not execute buddy view logic")
            return abort(500)

    #### HELPER FUNCTIONS

    def get_gender_definitions(self):
        """Get a list of all possible gender types"""
        try:
            return ["Male", "Female", "Other", "Prefer not to say"]

        except Exception as e:
                self._log.exception("Could not execute user get gender definitions logic")
                return abort(500)

    def get_data_definitions(self, scheme_id):
        """ Get a list of all possible hobbies and interests """
        try:
            data_definitions = {
                "hobbies": self._hobby_handler.get_hobby_list(scheme_id),
                "interests": self._interest_handler.get_interest_list(scheme_id)
            }

            return data_definitions

        except Exception as e:
                self._log.exception("Could not execute user get data definitions logic")
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
            self._scheme_handler = SchemeModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(500)

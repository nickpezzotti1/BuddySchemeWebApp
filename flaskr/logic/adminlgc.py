from flask import flash, redirect, render_template, request, url_for, abort, current_app
from flask_login import current_user
import logging
import json
import requests
from flaskr.auth_token import generate_token
from flaskr.emailer import send_email_scheme_invite
from flaskr.models.allocationconfigmdl import AllocationConfigModel
from flaskr.models.allocationmdl import AllocationModel
from flaskr.models.student_interestmdl import StudentInterestModel
from flaskr.models.student_hobbymdl import StudentHobbyModel
from flaskr.models.interestmdl import InterestModel
from flaskr.models.hobbymdl import HobbyModel
from flaskr.models.studentmdl import StudentModel
from datetime import date, datetime
from flaskr.forms import NewHobbyForm, NewInterestForm, AllocationConfigForm, InviteForm, DeleteHobbyForm, DeleteInterestForm



class AdminLogic:
    @staticmethod
    def admin_dashboard():
        """
        Redirects the admin back to the dashboard
        :return: dashboard.html
        """
        return render_template('admin/dashboard.html', title='Admin Dashboard')

    def admin_view_students(self):
        """
        Retrieves the students from the database for the specific scheme which the admin looks over and lists them
        with the option to request further information
        :return: view_students.html
        """
        try:
            data = self._student_handler.get_all_students_data_basic(current_user.scheme_id)
            return render_template('admin/view_students.html', title='View Students', data=data)
        except Exception:
            self._log.exception("Could not execute admin view")
            return abort(500)

    def view_student_details(self):
        """
        Returns the details about a specific student using their k-number to send a request form retrieving the associated data
        It allows the admin to change the admin status of the user and also manually assign them to a mentor/mentee as well giving the
        option to delete the user from the database.
        :return: student_details.html or 500 error code
        """
        try:
            if(request.method == 'POST' and 'knum' in request.form):
                k_number = request.form['knum']
                if('mkAdmin' in request.form):
                    res = self._student_handler.alter_admin_status(current_user.scheme_id, k_number, True)
                elif('rmAdmin' in request.form):
                    res = self._student_handler.alter_admin_status(current_user.scheme_id, k_number, False)
                elif('mkAlloc' in request.form):
                    torNum = request.form['torNum']
                    teeNum = request.form['teeNum']
                    res = self._allocation_handler.make_manual_allocation(current_user.scheme_id, teeNum, torNum)
                elif("rmAlloc" in request.form):
                    torNum = request.form['torNum']
                    teeNum = request.form['teeNum']
                    res = self._allocation_handler.remove_allocation(current_user.scheme_id, teeNum, torNum)
                udata = self.get_all_user_data(current_user.scheme_id, k_number)
                isTor = udata['is_mentor']
                if isTor:
                    matches = self._allocation_handler.get_mentee_details(current_user.scheme_id, k_number)
                else:
                    matches = self._allocation_handler.get_mentor_details(current_user.scheme_id, k_number)
                return render_template('admin/student_details.html', title='Details For ' + k_number, udata=udata, matches=matches) ## add scheme name to title?
            else:
                return redirect(url_for('admin.admin_view_students'))
        except Exception:
            self._log.exception("Could not execute student details")
            return abort(500)

    def delete_student_details(self):
        """
        Allows the admin to delete a user from the scheme by using their associated k-number
        If the admin attempts to delete their own account they will be redirected to their dashboard where they can
        delete their own account using their k-number
        :return: dashboard.html or 500 error code
        """
        try:
            if(request.method == 'POST' and 'knum' in request.form):
                k_number = request.form['knum']
                if current_user.k_number != k_number:
                    flash(k_number + "was deleted successfully")
                    res = self._student_handler.delete_students(current_user.scheme_id, k_number)
                else:
                    flash("Be careful! you are about to delete your own account," +
                        " if you wish to do so, do it from your user dashboard")
                return render_template("admin/dashboard.html", title="Admin Dashboard")

        except Exception:
            self._log.exception("Could not execute delete student details")
            return abort(500)

    def general_settings(self):
        """
        Retrieves the listed hobbies and interests associated with a given scheme and displays them
        Gives the admin the option to add further hobbies and interests using a request form, checks it doesn't exist alrady
        Page refreshes listing the new list of hobbies/interests
        :return: general_settings.html
        """
        try:
            new_hobby_form = NewHobbyForm(request.form)
            new_interest_form = NewInterestForm(request.form)
            
            if new_hobby_form.hobby_name.data:
                if new_hobby_form.validate_on_submit():
                    response = self._hobby_handler.get_hobby_list(current_user.scheme_id)
                    exists = False

                    for hobby in response:
                        if new_hobby_form.hobby_name.data == hobby["hobby_name"]:
                            exists = True

                    if exists:
                        flash("Hobby already created")
                    else:
                        flash("Hobby successfully created")
                        self._hobby_handler.insert_hobby(current_user.scheme_id, new_hobby_form.hobby_name.data)
                else:
                    flash("Error creating hobby")

            if new_interest_form.interest_name.data:
                if new_interest_form.validate_on_submit():
                    response = self._interest_handler.get_interest_list(current_user.scheme_id)
                    exists = False

                    for interest in response:
                        if new_interest_form.interest_name.data == interest["interest_name"]:
                            exists = True

                    if exists:
                        flash("Interest already created")
                    else:
                        flash("Interest successfully created")
                        self._interest_handler.insert_interest(current_user.scheme_id, new_interest_form.interest_name.data)
            

            delete_hobby_form = DeleteHobbyForm(request.form)
            if delete_hobby_form.hobby.data:
                delete_id = delete_hobby_form.hobby.data
                if self._hobby_handler.delete_hobby(current_user.scheme_id, delete_id):
                    flash("Hobby Removed")
                else:
                    flash("Unable To Remove Hobby")
                
            delete_interest_form = DeleteInterestForm(request.form)
            if delete_interest_form.interest.data:
                delete_id = delete_interest_form.interest.data
                if self._interest_handler.delete_interest(current_user.scheme_id, delete_id):
                    flash("Interest Removed")
                else:
                    flash("Unable To Remove Interest")

            currentHobbies = self._hobby_handler.get_hobby_list(current_user.scheme_id)
            delete_hobby_form.hobby.choices = [(h['id'], h['hobby_name']) for h in currentHobbies]
            currentInterests = self._interest_handler.get_interest_list(current_user.scheme_id)
            delete_interest_form.interest.choices = [(i['id'], i['interest_name']) for i in currentInterests]
            
            return render_template("admin/general_settings.html", hobby_form=new_hobby_form, delete_hobby_form=delete_hobby_form, delete_interest_form=delete_interest_form, interest_form=new_interest_form, currentHobbies=currentHobbies, currentInterests=currentInterests)

        except Exception:
            self._log.exception("Invalid new hobby form")
            return abort(500)

    def allocation_config(self):
        """
        Allows the admin to changes the weights of the allocatio algorithm
        Uses a post request and updates the page under the scheme id
        :return: allocation_config.html
        """
        # Retrieve current allocation config data
        config_data = self._allocation_config_handler.get_allocation_config(current_user.scheme_id)

        form = AllocationConfigForm(request.form, age_weight=config_data['age_weight'], gender_weight=config_data['gender_weight'], hobby_weight=config_data['hobby_weight'], interest_weight=config_data['interest_weight'])

        if(request.method == 'POST'):
            # Format the results in a dict and call the update query
            config = {
                'age_weight': form.age_weight.data,
                'gender_weight': form.gender_weight.data,
                'hobby_weight': form.hobby_weight.data,
                'interest_weight': form.interest_weight.data,
            }

            self._allocation_config_handler.update_allocation_config(current_user.scheme_id, config)

            # Text displayed after updating the config - as feedback for the user
            update_message = 'Configuration Updated'
        else:
            update_message = ''

        # Always render the page

        return render_template('admin/allocation_config.html',
            title='Allocation Algorithm', form=form,
            allocation_config=config_data, update_message=update_message)

    def allocation_algorithm(self):
        """
        Runs the allocation algorithm and sends the admin back to the dashboard
        Flashes it was successful
        :return: dashboard.html
        """
        flash("The allocations have been made, please look at the student table for more information")
        return render_template('admin/dashboard.html', assignments=self.allocate())

    def allocate(self):
        """
        Runs the allocation algorithm using the json provided from another method and returns the matches as a json
        :return: json
        """
        try:
            input_string = self.generate_mentee_and_mentor_json()

            response = requests.post(
                'https://c4t2nyi7y4.execute-api.us-east-2.amazonaws.com/default', data=input_string)
            # remove surrounding quotes (first and last char) and remove the backslashes (ASK NICHOLAS, problem with aws formatting)
            response_text = response.text[1:-1].replace("\\", "")
            json_response = json.loads(response_text)
            pairs = json_response["assignments"]

            try:
                # Clear the current allocations in the database
                self._allocation_handler.clear_allocations_table(current_user.scheme_id)

                # Insert the new allocations
                for pair in pairs:
                    self._allocation_handler.insert_mentor_mentee(
                        current_user.scheme_id, pair["mentor_id"], pair["mentee_id"])
            except:
                print("Error in inserting into db")



        except Exception as e:
            self._log.exception(e)
            return abort(500)

    def generate_mentee_and_mentor_json(self):
        """
        Retrieves the mentor, mentees with their associated data and submits them as a json
        :return: json
        """
        # Get allocation configuration from database
        allocation_config = self._allocation_config_handler.get_allocation_config(
            current_user.scheme_id)

        # Get all mentors from database
        mentors = self._allocation_handler.get_all_mentors(current_user.scheme_id)

        # Get all mentees from database
        mentees = self._allocation_handler.get_all_mentees(current_user.scheme_id)

        input = {"configurations": {
            "age_importance": allocation_config["age_weight"],
            "gender_importance": allocation_config["gender_weight"],
            "hobby_importance": allocation_config["hobby_weight"],
            "interest_importance": allocation_config["interest_weight"]
        }, "mentors": [], "mentees": []}

        for mentor in mentors:
            input["mentors"].append(
                {
                    "ID": mentor["k_number"],
                    "age": (-1 if mentor["date_of_birth"] is None else (date.today().year - datetime.strptime(str(mentor["date_of_birth"]), "%Y-%m-%d").year)),
                    "gender": mentor["gender"],
                    "partnerLimit": mentor["buddy_limit"]
                }
            )

        for mentee in mentees:
            input["mentees"].append(
                {
                    "ID": mentee["k_number"],
                    "age": (-1 if mentee["date_of_birth"] is None else (date.today().year - datetime.strptime(str(mentee["date_of_birth"]), "%Y-%m-%d").year)),
                    "gender": mentee["gender"],
                    "partnerLimit": mentee["buddy_limit"]
                }
            )

        return json.dumps(input)

    def manually_assign(self):
        """
        Allows the admin manually assign a mentee/mentor using their k-number.
        Restricts assignment of mentor-mentor, mentee-mentee and already matches users
        :return: manually_assign.html
        """
        try:
            if(request.method == 'POST'):
                k_number = request.form['knum']
                udata = self._student_handler.get_user_data(current_user.scheme_id, k_number)
                potentials = self._allocation_handler.get_manual_allocation_matches(
                    current_user.scheme_id, k_number, udata['is_mentor'])
                # imprv title?
                return render_template('admin/manually_assign.html', title='Manually Assign Match', udata=udata, potentials=potentials)
            else:
                return redirect(url_for('admin.admin_view_students'))

        except Exception:
            self._log.exception("Could not execute manual assignment")
            flash("Something went wrong during manual assignment")

    def get_all_user_data(self, scheme_id, k_number):
        """ Get all user data from database and format into a single dict
        :rtype: object
        """
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

        except Exception:
            self._log.exception("Could not execute get all user data logic")
            return abort(500)

    def invite_to_scheme(self):
        """
        Generates a url to allow users to sign up to the specific scheme using the scheme_id
        :return: invite.html
        """
        invite_form = InviteForm()
        scheme_id = current_user.scheme_id
        token = generate_token(secret_key=current_app.config["SECRET_KEY"], message=scheme_id)
        invite_url = current_app.config["WEBSITE_PATH"] + "signup/" + token

        if request.method == 'POST':
            if invite_form.validate_on_submit:
                email = invite_form.email.data
                send_email_scheme_invite(email=email, token=token)
                flash("Invite sent.")

        return render_template('admin/invite.html', title='Invite to scheme', invite_form=invite_form, invite_url=invite_url)

    def __init__(self):
        try:
            self._log = logging.getLogger(__name__)
            self._allocation_config_handler = AllocationConfigModel()
            self._allocation_handler = AllocationModel()
            self._student_handler = StudentModel()
            self._student_hobby_handler = StudentHobbyModel()
            self._student_interest_handler = StudentInterestModel()
            self._hobby_handler = HobbyModel()
            self._interest_handler = InterestModel()
        except Exception:
            self._log.exception("Could not create model instance")
            raise abort(500)

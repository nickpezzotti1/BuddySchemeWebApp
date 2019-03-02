from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging
import json
import requests
from models.allocationconfigmdl import AllocationConfigModel
from models.allocationmdl import AllocationModel
from models.student_interestmdl import StudentInterestModel
from models.student_hobbymdl import StudentHobbyModel
from models.interestmdl import InterestModel
from models.hobbymdl import HobbyModel
from models.studentmdl import StudentModel

class AdminLogic():


    def admin_dashboard(self):
        return render_template('admin/dashboard.html', title='Admin Dashboard')


    def admin_view_students(self):
        try:
            data = self._student_handler.get_all_students_data_basic()
            return render_template('admin/view_students.html', title='View Students', data=data)
        except Exception as e:
            self._log.exception("Could not execute admin view")
            return abort(404)


    def view_student_details(self):
        try:
            if(request.method == 'POST' and 'knum' in request.form):
                kNum = request.form['knum']
                if('mkAdmin' in request.form):
                    res = self._student_handler.alter_admin_status(kNum, True)
                elif('rmAdmin' in request.form):
                    res = self._student_handler.alter_admin_status(kNum, False)
                elif('mkAlloc' in request.form):
                    torNum = request.form['torNum']
                    teeNum = request.form['teeNum']
                    res = self._allocation_handler.make_manual_allocation(teeNum, torNum)
                elif("rmAlloc" in request.form):
                    torNum = request.form['torNum']
                    teeNum = request.form['teeNum']
                    res = self._allocation_handler.remove_allocation(teeNum, torNum)
                udata = self._student_handler.get_user_data(kNum)
                hobbies = self._hobbies_handler.get_hobbies(kNum)
                interests = self._interest_handler.get_interests(kNum)
                isTor = udata['is_mentor']
                if isTor:
                    matches = self._allocation_handler.get_mentee_details(kNum)
                else:
                    matches = self._allocation_handler.get_mentor_details(kNum)
                return render_template('admin/student_details.html', title='Details For ' + kNum, udata=udata, hobbies=hobbies, interests=interests, matches=matches)
            else:
                return redirect(url_for('admin.admin_view_students'))

        except Exception as e:
            self._log.exception("Could not execute student details")
            return abort(404)


    def delete_student_details(self):

        try:
            if(request.method == 'POST' and 'knum' in request.form):
                kNum = request.form['knum']
                res = self._student_handler.delete_students(kNum)
                return render_template('admin/delete_student.html', title='Delete Student Profile ' + kNum, res=res, k_number=kNum)
            else:
                return redirect(url_for('admin.admin_view_students'))

        except Exception as e:
            self._log.exception("Could not execute delete student details")
            return abort(404)


    def general_settings(self):

        return render_template('admin/general_settings.html', title='General Settings')


    def allocation_config(self):
        if(request.method == 'POST'):
            # Format the results in a dict and call the update query
            config = {
                'age_weight': request.form['age_weight'],
                'gender_weight': request.form['gender_weight'],
                'hobby_weight': request.form['hobby_weight'],
                'interest_weight': request.form['interest_weight'],
            }

            self._allocation_config_handler.update_allocation_config(config)

            # Text displayed after updating the config - as feedback for the user
            update_message = 'Configuration Updated'
        else:
            update_message = ''

        # Always render the page
        allocation_config = self._allocation_config_handler.get_allocation_config()

        return render_template('admin/allocation_config.html', title='Allocation Algorithm', allocation_config=allocation_config, update_message=update_message)

    def allocation_algorithm(self):
        return render_template('admin/allocation_algorithm.html', title='Allocation Algorithm', assignments=self.allocate())

    def sign_up_settings(self):
        return render_template('admin/dashboard.html', title='Sign-Up Settings')


    def allocate(self):

        try:
            input_string = self.generate_mentee_and_mentor_json()

            response = requests.post('https://c4t2nyi7y4.execute-api.us-east-2.amazonaws.com/default', data=input_string)
            # remove surrounding quotes (first and last char) and remove the backslashes (ASK NICHOLAS, problem with aws formatting)
            response_text = response.text[1:-1].replace("\\", "")
            json_response = json.loads(response_text)
            pairs = json_response["assignments"]

            try:
                for pair in pairs:
                    self._allocation_handler.insert_mentor_mentee(pair["mentor_id"], pair["mentee_id"])
            except:
                print("Error in inserting into db")

            return "The following assignments have been made:" + str(json_response["assignments"])

        except Exception as e:
            self._log.exception(e)
            return e

    #TODO add try catch for this method
    def generate_mentee_and_mentor_json(self):
        
        # Get allocation configuration from database
        allocation_config = self._allocation_config_handler.get_allocation_config()

        # Get all mentors from database
        mentors = self._allocation_handler.get_all_mentors()

        # Get all mentees from database
        mentees = self._allocation_handler.get_all_mentees()

        input = {"configurations": {}, "mentors": [], "mentees": []}

        input["configurations"] = {
            "age_importance": allocation_config["age_weight"],
            "sex_importance": allocation_config["gender_weight"],
            "hobby_importance": allocation_config["hobby_weight"],
            "interest_importance": allocation_config["interest_weight"]
        }

        for mentor in mentors:
            input["mentors"].append(
                                    {
                                        "ID": mentor["k_number"],
                                        "age": 20,
                                        "isMale": True,
                                        "menteeLimit": 1
                                    }
                                )

        for mentee in mentees:
            input["mentees"].append(
                                    {
                                        "ID": mentee["k_number"],
                                        "age": 20,
                                        "isMale": True
                                    }
                                )

        return json.dumps(input)



    def manually_assign(self):

        try:
            if(request.method == 'POST'):
                kNum = request.form['knum']
                udata = self._student_handler.get_user_data(kNum)
                potentials = self._allocation_handler.get_manual_allocation_matches(kNum, udata['is_mentor'])
                return render_template('admin/manually_assign.html', title='Manually Assign Match', udata=udata, potentials=potentials) # imprv title?
            else:
                return redirect(url_for('admin.admin_view_students'))

        except Exception as e:
            self._log.exception("Could not execute manual assignment")
            return abort(404)


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
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(404)

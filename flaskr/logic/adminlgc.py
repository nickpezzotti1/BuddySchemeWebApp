from flask import Flask, flash, redirect, render_template, request, url_for, Blueprint, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import logging
import json
from models.allocationmdl import AllocationModel
from models.interestmdl import InterestModel
from models.hobbiesmdl import HobbiesModel
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

    
    def allocation_algorithm(self):
        return render_template('admin/allocation_algorithm.html', title='allocation_algorithm', assignments=self.allocate())

    
    def sign_up_settings(self):
        return render_template('admin/dashboard.html', title='Sign-Up Settings')

    
    def allocate(self):

        try:
            input_string = generate_mentee_and_mentor_json()

            response = requests.post('https://c4t2nyi7y4.execute-api.us-east-2.amazonaws.com/default', data=input_string)
            # remove surrounding quotes (first and last char) and remove the backslashes (ASK NICHOLAS, problem with aws formatting)
            response_text = response.text[1:-1].replace("\\", "")
            json_response = json.loads(response_text)
            pairs = json_response["assignments"]

            try:
                for pair in pairs:
                    self._allocation_handler.insert_mentor_mentee("k" + pair["mentor_id"], "k" + pair["mentee_id"])
            except:
                print("Error in inserting into db")

            return "The following assignments have been made:" + str(json_response["assignments"])

        except Exception as e:
            self._log.exception("Could not execute update user preferences logic")
            return "Error"

    def generate_mentee_and_mentor_json(self):

        try:
            # Get all mentors from database
            mentors = self._allocation_handler.get_all_mentors()

            # Get all mentees from database
            mentees = self._allocation_handler.get_all_mentees()

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

        except Exception as e:
            self._log.exception("Could not execute generate mentor mentee json")
            return "Error"

    
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
            self._allocation_handler = AllocationModel()
            self._student_handler = StudentModel()
            self._hobbies_handler = HobbiesModel()
            self._interest_handler = InterestModel()
        except Exception as e:
                self._log.exception("Could not create model instance")
                return abort(404)




from flask import request
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from flaskr.models.schememdl import SchemeModel
from flaskr.models.studentmdl import StudentModel


class User(UserMixin):

    def get(cookie_string):
        split_pos = cookie_string.find(":")
        p1 = cookie_string[:split_pos]
        p2 = cookie_string[(split_pos + 1):]
        return SystemAdmin(p2) if p1 == 'sysadmin' else Student(p1, p2)


class Student(User):
    def __init__(self, scheme_id, k_number):
        self._student_handler = StudentModel()

        self.scheme_id = scheme_id
        self.k_number = k_number
        self.id = str(scheme_id) + ":" + k_number
        self.password = None
        self.email_confirmed = False
        self.role = "mentee"
        self.priv = "student"

        try:
            self.password = self._student_handler.get_user_hashed_password(
                scheme_id, k_number)
            user_data = self._student_handler.get_user_data(
                scheme_id, k_number)

        except Exception as e:
            print("Exeception occured:{}".format(e))

        if not bool(user_data["email_confirmed"]):
            raise Exception("User needs to confirm his email")

        self.email_confirmed = bool(user_data["email_confirmed"])
        self.role = 'mentor' if user_data["is_mentor"] else "mentee"
        self.priv = 'admin' if user_data["is_admin"] else "student"

    @property
    def is_active(self):
        # user only able to login if email is confirmed
        return True  # self.email_confirmed

    def activate(self):
        # activates user account in database
        self._student_handler.activateAccount(
            scheme_id=self.scheme_id, k_number=self.k_number)

    def reset_password(self, new_password):
        new_hashed_password = generate_password_hash(
            new_password, method="")  # don't use sha256
        self.password = new_hashed_password
        print("after " + new_hashed_password)
        self._student_handler.update_hash_password(
            scheme_id=self.scheme_id, k_number=self.k_number, password_hash=new_hashed_password)


class SystemAdmin(User):
    def __init__(self, email):
        User.__init__(self)
        self._scheme_handler = SchemeModel()  # change?
        # can be any -> set to first in DB to prevent errors
        self.scheme_id = request.cookies.get(
            'scheme') if 'scheme' in request.cookies else 1
        self.k_number = 69  # needed?
        self.id = "sysadmin:" + email
        self.password = None
        self.priv = "system_admin"

        try:
            self.password = self._scheme_handler.get_system_admin_pass(email)

        except Exception as e:
            print("Exeception occured:{}".format(e))

    @property
    def is_active(self):
        return True

    def set_scheme_id(self, scheme_id):
        self.scheme_id = scheme_id

    def reset_password(self, new_password):
        new_hashed_password = generate_password_hash(new_password, method="")
        self.password = new_hashed_password
        print("after " + new_hashed_password)
        # self._student_handler.update_hash_password(scheme_id=self.scheme_id, k_number=self.k_number, password_hash=new_hashed_password)## needs changing

import basic as db
from flask_login import UserMixin
from models.studentmdl import StudentModel
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self, scheme_id, k_number):
        self._student_handler = StudentModel()
        
        self.scheme_id = scheme_id
        self.k_number = k_number
        self.id = str(scheme_id) + ":" + k_number
        self.password = None
        self.email_confirmed = False
        self.role = "ADMIN" ###

        try:
            self.password = self._student_handler.get_user_hashed_password(scheme_id, k_number)
            self.email_confirmed = bool(self._student_handler.get_user_data(scheme_id, k_number)["email_confirmed"])

        except Exception as e:
            print("Exeception occured:{}".format(e))

    @property
    def is_active(self):
        # user only able to login if email is confirmed
        return True  ##self.email_confirmed

    

    def activate(self):
        # activates user account in database
        self._student_handler.update_students(scheme_id=self.scheme_id, k_number=self.k_number, email_confirmed=True)

    def reset_password(self, new_password):
        new_hashed_password = generate_password_hash(new_password, method="") ### don't use sha256
        self.password = new_hashed_password
        print("after " + new_hashed_password)
        self._student_handler.update_hash_password(scheme_id=self.scheme_id, k_number=self.k_number, password_hash=new_hashed_password)

    
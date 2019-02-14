from flask_login import UserMixin
import basic as db

class User(UserMixin):
    def __init__(self, k_number):
        self.k_number = k_number
        self.id = k_number
        self.password = None

        try:
            self.password = db.get_user_hashed_password(k_number)["password_hash"]

        except Exception as e:
            print("Exeception occured:{}".format(e))


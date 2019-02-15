from flask_login import UserMixin
import basic as db

class User(UserMixin):
    def __init__(self, k_number):
        self.k_number = k_number
        self.id = k_number
        self.password = None
        self.confirmed_email = None

        try:
            self.password = db.get_user_hashed_password(k_number)
            self.confirmed_email = db.get_user_data(k_number).confirmed_email["email_confirmed"]

        except Exception as e:
            print("Exeception occured:{}".format(e))
    
    @property
    def is_active(self):
        # user only able to login if email is confirmed
        return self.confirmed_email
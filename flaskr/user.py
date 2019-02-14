from flask_login import UserMixin
import basic as db

class User(UserMixin):
    ## TODO: implement query database
    # k_number = "k1764171"
    # hashed password "12345678"
    # password = "pbkdf2:sha256:50000$zP6dR6Ek$e54364ebb8f1d5c7f730781fe0609e0dfaa030a124719269329a650e7b7a25ee"
    # id == k_number
    
    def __init__(self, k_number):
        self.k_number = k_number
        self.id = k_number
        self.password = db.get_user_hashed_password(k_number)["password_hash"]
        

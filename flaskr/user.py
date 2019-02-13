from flask_login import UserMixin

class User(UserMixin):
    ## TODO: implement query database
    k_number = "k1764171"
    # hashed password "12345678"
    password = "pbkdf2:sha256:50000$zP6dR6Ek$e54364ebb8f1d5c7f730781fe0609e0dfaa030a124719269329a650e7b7a25ee"
    # id == k_number
    id = k_number

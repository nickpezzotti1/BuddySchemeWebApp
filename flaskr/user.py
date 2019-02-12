from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    # query database

    # user_info = getMenteeData(k_number): Dictionary
            # Query database with k number to get the following fields:
                # k number: string
                # First Name: string
                # Last Name: string
                # Age: int
                # Hobbies: List[string]
                # Academic interests: List[string]

    ## TODO: Use Nihad's columns
    k_number = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(15))
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    age = db.Column(db.Integer(15))
    hobbies = db.Column(db.String(15))
    academic_interests = db.Column(db.String(15))
    is_active = True
    is_anonymous = False

    # id == k_number
    id = k_number

    def is_authenticated():
        # query database
        return True
    
    def is_active():
        # query database
        return is_active

    def is_anonymous():
        return is_anonymous
    
    def get_id():
        return k_number

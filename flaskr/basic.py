import os
import pymysql

# Will set up the credentials
DATABASE_USER = os.environ.get("BUDDY_DB_USER", '')
DATABASE_PASSWORD = os.environ.get("BUDDY_DB_PASSWORD", '')
DB_NAME = "Buddy"
DB_HOST = "buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com"

HASH_COL = 'password_hash'

def _query(sql_query):
    """ Returns results of query """
    
    # Connect to the database
    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)

    # Define result
    result = ""   

    try:
    
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

    except Exception as e:
        print("Exeception occured:{}".format(e))

    finally:
        conn.close()

    return result


def _insert(sql_query):
    """ Will push a query to the DB"""    

    # Connect to the database
    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)

    try:
        with conn.cursor() as cursor:
            result = cursor.execute(sql_query)

        conn.commit()
            
    except Exception as e:
        print("Exeception occured:{}".format(e))
        return False

    finally:
        conn.close()
    
    return True


def _sanity_check(sql_fields):
    """ Will sanity check the fields 
        return true, if we can run it"""

    return (type(sql_fields) == int) or sql_fields.replace(" ", "").isalnum()


def _to_str(my_str):
    """ Will return the string surrounded by 
        double quotes, useful for SQL query"""

    if type(my_str) == str:
        return "\"" + my_str + "\""
    else:
        return f"Error: {my_str} isn't a string"


# TODO should I raise my own exception?
def _update_students(** kwargs):
    """ Will update fields in Students based on the k_number
        You will need to precise the specific field"""

    accepted_fields = {"first_name":"", "last_name":"", "degree_title":"",
        "year_study":0, "gender":"", "k_number":""}
    
    sql_query = ""

    # We need the k_number to update
    if "k_number" not in kwargs:
        return "Error: k_number not defined"
    
    # Will check that the field is valid, only alphanum and right type
    for field, value in kwargs.items():

        if not _sanity_check(value):
            return f"Error: {field} did not pass sanity check"
        elif field not in accepted_fields:
            return f"Error: {field} isn't a column in the table"
        elif type(value) != type(accepted_fields[field]):
            return f"Error: {field} is the wrong type"


    # Ie if there's k_number and another field to update 
    if len(kwargs) > 1:
        sql_query = "UPDATE Students set "
        sql_query += ", ".join([f"{field} = {_to_str(value) if type(value)==str else int(value) }" for field, value in kwargs.items() if field != "k_number"])
        sql_query += f" where k_number={_to_str(kwargs['k_number'])};" 
    else:
        return "Error: did not pass enough arguments"

    return _insert(sql_query)


# TODO should I raise my own exception?
def _update_informations(** kwargs):
    """ Will update hobbies and interests in Students based on the k_number
        You will need to precise the specific field"""

    accepted_fields = {"hobbies":"", "interests":"", "k_number":""}    
    sql_query = ""

    # We need the k_number to update
    if "k_number" not in kwargs:
        return "Error: k_number not defined"
    
    # Will check that the field is valid, only alphanum and right type
    for field, value in kwargs.items():

        if not _sanity_check(value):
            return f"Error: {field} did not pass sanity check"
        elif field not in accepted_fields:
            return f"Error: {field} isn't a column in the table"
        elif type(value) != type(accepted_fields[field]):
            return f"Error: {field} is the wrong type"


    # Ie if there's k_number and another field to update 
    if len(kwargs) > 1:
        sql_query = "UPDATE Informations set "
        sql_query += ", ".join([f"{field} = {_to_str(value) if type(value)==str else int(value) }" for field, value in kwargs.items() if field != "k_number"])
        sql_query += f" where k_number={_to_str(kwargs['k_number'])};" 
    else:
        return "Error: did not pass enough arguments"

    return _insert(sql_query)

# TODO check the 0 and 1 return 
def update_students(k_number, first_name=False, last_name=False, degree_title=False, year_study=False, gender=False):
    """ Front end interface of the private function, 
        don't need to know the underlying interface """

    accepted_fields = {"k_number": k_number, "first_name": first_name, "last_name": last_name, "degree_title": degree_title, "year_study": year_study}

    # Set the dictionarry like it's needed
    dict_fields = {field:value for field, value in  accepted_fields.items() if value is not False}

    return _update_students(** dict_fields)

def update_informations(k_number, hobbies=False, interests=False):
    """ Given either or hobbies and interests,
        Will update the entry based on the k_number
        Return True if no errors while updating, False otherwise"""

    accepted_fields = {"k_number": k_number, "hobbies":hobbies, "interests":interests} 

    # Set the dictionnary like it's needed
    dict_fields = {field:value for field, value in accepted_fields.items() if value is not False}

    return _update_informations(** dict_fields)

def update_mentor(mentor_k_number, mentee_k_number):
    """ Given both mentor and mentee k_number,
        Will update the mentor"""

    if _sanity_check(mentor_k_number) and _sanity_check(mentee_k_number):
        return _insert(f"UPDATE Allocation set mentor_k_number={_to_str(mentor_k_number)} where mentee_k_number={_to_str(mentee_k_number)};")
    else:
        return "Error: one of the k_number did not pass the sanity check"


def update_mentee(mentor_k_number, mentee_k_number):
    """ Given both mentee and mentor k_number,
        Will update the mentee"""

    if _sanity_check(mentor_k_number) and _sanity_check(mentee_k_number):
        return _insert(f"UPDATE Allocation set mentee_k_number={_to_str(mentee_k_number)} where mentor_k_number={_to_str(mentor_k_number)};")
    else:
        return "Error: one of the k_number did not pass sanity check"
 

def get_user_data(k_number):
    """ Returns all the data in the Students table except from password hash"""
    
    if _sanity_check(k_number):
        result = _query(f"SELECT * FROM Students where k_number={_to_str(k_number)};")[0]
        result.pop(HASH_COL, None) # can check not none
        return result       
    else:
        return "Error: k_number did not pass sanity check"


def get_user_hashed_password(k_number):
    """ Returns the hashed password for the user"""

    if _sanity_check(k_number):
        result = _query(f"select password_hash from Students where k_number={_to_str(k_number)};")
        return result[0].pop(HASH_COL, None) 
    else:
        return "Error: k_number did not pass sanity check"


def get_mentors(mentee_k_number):
    """ Given the mentee K-Number will return its mentor(s) k-number"""

    if _sanity_check(mentee_k_number):
        result = _query(f"SELECT mentor_k_number from Allocation where mentee_k_number={_to_str(mentee_k_number)};")
        return result
    else:
        return "Error: k_number did not pass sanity check"


def get_mentees(mentor_k_number):
    """ Given the mentor K-Number will return its mentor(s) k-number"""

    if _sanity_check(mentor_k_number):
        result = _query(f"SELECT mentee_k_number from Allocation where mentor_k_number={_to_str(mentor_k_number)};")
        return result
    else:
        return "Error: k_number did not pass sanity check"


def get_information(k_number): #### change this to two -> hobbies + interests
    """ Given the k_number will return all the extra information on that student
        As a dictionnary"""

    if _sanity_check(k_number):
        result = _query(f"select * from Informations where k_number={_to_str(k_number)};")
        return result
    else:
        return "Error: the k_number did not pass the sanity check"


def insert_mentor_mentee(mentor_k_number, mentee_k_number):
    """ Insert the mentor, mentee pair k number """

    if _sanity_check(mentor_k_number) and _sanity_check(mentee_k_number):
        return _insert(f"INSERT INTO Allocation VALUES({_to_str(mentor_k_number)}, {_to_str(mentee_k_number)});")
    else:
        return "Error: one of the k_number did not pass sanity check"


def insert_student(k_number, first_name, last_name, degree_title, year_study, gender, password_hash):
    """ Will entirely populate an entry for Students table"""

    if _sanity_check(k_number) and _sanity_check(first_name) and _sanity_check(last_name) and _sanity_check(degree_title) and _sanity_check(year_study) and _sanity_check(gender):
        value = f"INSERT INTO Students VALUES({_to_str(k_number)}, {_to_str(first_name)}, {_to_str(last_name)}, {_to_str(degree_title)}, {year_study}, {_to_str(gender)}, 0, 0, {_to_str(password_hash)});"
        print(value)
        return _insert(value)
    else:
        return "Error: one of the field did not pass sanity check"


def insert_interests(k_number, hobbies, interests):
    """ Will entirely populate an entry for Information table
        Returns True if everything went correctly, False otherwise"""
    
    if _sanity_check(k_number) and _sanity_check(hobbies) and _sanity_check(interests):
        return _insert(f"INSERT INTO Informations VALUES({_to_str(hobbies)}, {_to_str(interests)}, {_to_str(k_number)});")
    else:
        return "Error: one of the field did not pass the sanity check"


def get_all_students_data_basic():
    return _query("SELECT k_number, first_name, last_name, CASE WHEN (year_study > 1) THEN TRUE ELSE FALSE END AS is_mentor FROM Students ORDER BY last_name ASC;")   ## add has matches 

def get_mentee_details(k_number):
    if _sanity_check(k_number): 
        return _query(f"SELECT k_number, first_name, last_name FROM Students, Allocation WHERE Students.k_number = Allocation.mentee_k_number AND Allocation.mentor_k_number = {_to_str(k_number)};")
    else:
        return "Error: one of the field did not pass the sanity check"


if __name__ == '__main__':
    pass

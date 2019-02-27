import os
import pymysql

# Will set up the credentials
DATABASE_USER = os.environ.get("BUDDY_DB_USER", '')
DATABASE_PASSWORD = os.environ.get("BUDDY_DB_PASSWORD", '')
DB_NAME = "Buddy"
DB_HOST = "buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com"

HASH_COL = 'password_hash'

def _query(sql_query):
    """ Returns a list of results of query """

    # Connect to the database
    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)

    # Define result
    result = []

    try:

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

    except Exception as e:
        raise Exception(f"{e}")

    finally:
        conn.close()

    # Empty answer will be tuple
    if type(result) == tuple:
        return []
    else:
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
        raise Exception(f"{e}")
        return False

    finally:
        conn.close()

    return True


def _sanity_check(sql_fields):
    """ Will sanity check the fields
        return true, if we can run it"""

    if (type(sql_fields) in [int, bool]) or sql_fields.replace(" ", "").isalnum():
        return True
    else:
        raise ValueError(f"{sql_fields} isn't an accepted field value.")


def _to_str(my_str, password_hash=False):
    """ Will return the string surrounded by
        double quotes, useful for SQL query
        Or if it's a bool return TRUE/FALSE
        Or if it's a number the number as it is
        Or if it's a list will call back this function
        and return all the field separated by ',' """

    if password_hash:
        return "\"" + my_str + "\""

    if type(my_str) is list:
        return ",".join([_to_str(i) for i in my_str])

    if _sanity_check(my_str):
        if type(my_str) is str:
            return "\"" + my_str + "\""
        elif type(my_str) is int:
            return str(my_str)
        # For better looking sql queries
        elif my_str is True:
            return 1
        elif my_str is False:
            return 0

    raise TypeError(f"{type(my_str)} type isn't accepted.")


def _update_students( ** kwargs):
    """ Will update fields in Students based on the k_number
        You will need to precise the specific field"""

    accepted_fields = {"first_name":str, "last_name":str, "degree_title":str,
        "year_study":int, "gender":str, "k_number":str, "is_mentor":bool,
        "email_confirmed": bool, "is_admin": bool}

    # We need the k_number to update
    if "k_number" not in kwargs:
        raise NameError("K-number could not be found in the list of arguments")

    # Will check that the field is valid, only alphanum and right type
    for field, value in kwargs.items():

        if field not in accepted_fields:
            raise Exception(f"{field} isn't a column in the table")
        elif type(value) != accepted_fields[field]:
            raise TypeError(f"{field} is the wrong type")

    # Ie if there's k_number and another field to update
    if len(kwargs) > 1:
        sql_query = "UPDATE Students set "
        sql_query += ", ".join([f"{field} = {_to_str(value)}" for field, value in kwargs.items() if field != "k_number"])
        sql_query += f" where k_number={_to_str(kwargs['k_number'])};"
        return _insert(sql_query)
    else:
        raise Exception("Need at least one argument.")



def update_students(k_number, first_name=[], last_name=[], degree_title=[], year_study=[], gender=[], is_mentor=[], is_admin=[], email_confirmed=[]):
    """ Front end interface of the private function,
        don't need to know the underlying interface """

    accepted_fields = {"k_number": k_number, "first_name": first_name,
        "last_name": last_name, "degree_title": degree_title,
        "year_study": year_study, "gender": gender, "is_mentor": is_mentor,
        "is_admin": is_admin, "email_confirmed": email_confirmed}

    # Set the dictionarry like it's needed
    dict_fields = {field:value for field, value in  accepted_fields.items() if type(value) is not list}

    return _update_students( ** dict_fields)


def update_hobbies(k_number, hobbies):
    """ Given the k_number and hobbies, will delete all the hobbies
        And reinsert them"""

    if type(hobbies) is not list:
        raise TypeError("Hobby/ies must be passed as a list.")

    delete_hobbies(k_number)

    for hobby in hobbies:
        insert_hobbies(k_number, hobby)

    return True


def update_interests(k_number, interests):
    """ Given the k-number of the students and new interests
        Will replace all the interests by the new one"""

    if type(interests) is not list:
        raise TypeError("Interest/s must be passed as a list")

    delete_interests(k_number)

    for interest in interests:
        insert_interests(k_number, interest)

    return True


def update_mentee(mentor_k_number, mentees_k_number):
    """ Given the mentor_k_number will update all his mentees"""

    if type(mentees_k_number) is not list:
        raise TypeError("Mentee/s must be passed as a list.")

    delete_mentees(mentor_k_number)

    for mentee_k_number in mentees_k_number:
        insert_mentor_mentee(mentor_k_number, mentee_k_number)

    return True


def update_mentor(mentee_k_number, mentors_k_number):
    """ Given the mentee_k_number will update all his mentors"""

    if type(mentors_k_number) is not list:
        raise TypeError("Mentor/s must be passed as a list.")

    delete_mentors(mentee_k_number)

    for mentor_k_number in mentors_k_number:
        insert_mentor_mentee(mentor_k_number, mentee_k_number)

    return True


def update_hash_password(k_number, password_hash):
    """ Given the k_number, will update the password_hash"""

    if type(password_hash) is str:
        password_hash_sql = "\"" + password_hash + "\""
        return _insert(f"UPDATE Students set password_hash={password_hash_sql};")
    else:
        raise TypeError(f"{type(password_hash)} type isn't accepted")


def get_user_data(k_number):
    """ Returns all the data in the Students table except from password hash"""

    try:
        result = _query(f"SELECT * FROM Students where k_number={_to_str(k_number)};")[0]
        result.pop(HASH_COL, None) # can check not none
        return result

    except IndexError:
        raise IndexError(f"{k_number} doesn't exist.")
    except KeyError:
        raise KeyError(f"{HASH_COL} not found in table.")

#TODO Should I return something here?


def get_user_hashed_password(k_number):
    """ Returns the hashed password for the user"""

    try:
        result = _query(f"select password_hash from Students where k_number={_to_str(k_number)};")
        return result[0].pop(HASH_COL, None)

    except IndexError:
        raise IndexError(f"{k_number} does not exist.")
    except KeyError:
        raise KeyError(f"{HASH_COL} not found in table")

# TODO Should I return something here as well?


def get_mentors(mentee_k_number):
    """ Given the mentee K-Number will return its mentor(s) k-number"""

    return _query(f"SELECT mentor_k_number from Allocation where mentee_k_number={_to_str(mentee_k_number)};")


def get_mentees(mentor_k_number):
    """ Given the mentor K-Number will return its mentor(s) k-number"""

    return _query(f"SELECT mentee_k_number from Allocation where mentor_k_number={_to_str(mentor_k_number)};")


def get_hobbies(k_number):
    """ Given the k_number will return all the student's hobbies"""

    return _query(f"SELECT * FROM Hobbies where k_number={_to_str(k_number)};")


def get_interests(k_number):
    """ Given the k_number will return all the student's interests"""

    return _query(f"SELECT * FROM Interests where k_number={_to_str(k_number)}")


def insert_mentor_mentee(mentor_k_number, mentee_k_number):
    """ Insert the mentor, mentee pair k number """

    return _insert(f"INSERT INTO Allocation VALUES({_to_str([mentor_k_number, mentee_k_number])});")


def insert_student(k_number, first_name, last_name, degree_title, year_study, gender, is_mentor, password_hash, is_admin):
    """ Will entirely populate an entry for Students table"""

    return _insert(f"INSERT INTO Students VALUES({_to_str([k_number, first_name, last_name, degree_title, year_study, gender, is_mentor])}, FALSE, {_to_str(password_hash, password_hash=True)}, {_to_str(is_admin)});")


def insert_hobby(k_number, hobby):
    """ Will entirely populate an entry for the Hobbies database"""

    return _insert(f"INSERT INTO Hobbies VALUES({_to_str([hobby, k_number])});")


def insert_interest(k_number, interest):
    """ Will entirely populate an entry for Interests table"""

    return _insert(f"INSERT INTO Interests VALUES({_to_str([interest, k_number])});")


# TODO Need to check for hobbies type
def delete_hobbies(k_number, hobbies=False):
    """ Will delete all the rows where K_number is
         Or only where hobbies and k-number are"""

    if hobbies:
        return _insert(f"DELETE FROM Hobbies where k_number={_to_str(k_number)} and hobby={_to_str(hobbies)};")
    else:
        return _insert(f"DELETE FROM Hobbies where k_number={_to_str(k_number)};")


def delete_interests(k_number, interests=False):
    """ Will delete all the rows where the k-number is
        Or only where interests and k-number are"""

    if interests:
        return _insert(f"DELETE FROM Interests where k_number={_to_str(k_number)} and interest={_to_str(interests)};")
    else:
        return _insert(f"DELETE FROM Interests where k_number={_to_str(k_number)};")


def delete_mentors(mentee_k_number):
    """ Given the mentee k-number will delete all his mentors"""

    return _insert(f"DELETE FROM Allocation where mentee_k_number={_to_str(mentee_k_number)};")

def delete_mentees(mentor_k_number):
    """ Given the mentor k-number will delete all his mentees"""

    return _insert(f"DELETE FROM Allocation where mentor_k_number={_to_str(mentor_k_number)};")


def delete_students(k_number):
    """ Delete the students entry in the Tables"""


    delete_hobbies(k_number)
    delete_interests(k_number)
    delete_mentors(k_number)
    delete_mentees(k_number)

    return _insert(f"DELETE FROM Students where k_number={_to_str(k_number)};")



def get_all_students_data_basic():
    """ God knows what this function does"""

    # Add has matches
    return _query("SELECT k_number, first_name, last_name, is_mentor FROM Students ORDER BY last_name ASC;")


def get_all_mentors():
    """ Returns all the k-number of mentors"""

    return _query("SELECT k_number FROM Students Where is_mentor=0;")


def get_all_mentees():
    """ Returns all the k-number of the mentees"""

    return _query("SELECT k_number FROM Students Where is_mentor=1;")



def get_all_students_data_basic():
    return _query("SELECT k_number, first_name, last_name, gender, is_mentor FROM Students ORDER BY last_name ASC;")   ## add has matches

def get_mentee_details(k_number):
    if _sanity_check(k_number):
        return _query(f"SELECT k_number, first_name, last_name, year_study FROM Students, Allocation WHERE Students.k_number = Allocation.mentee_k_number AND Allocation.mentor_k_number = {_to_str(k_number)};")
    else:
        return "Error: one of the field did not pass the sanity check"

def get_mentor_details(k_number):
    if _sanity_check(k_number):
        return _query(f"SELECT k_number, first_name, last_name, year_study FROM Students, Allocation WHERE Students.k_number = Allocation.mentor_k_number AND Allocation.mentee_k_number = {_to_str(k_number)};")
    else:
        return "Error: one of the field did not pass the sanity check"

def get_manual_allocation_matches(k_number, is_tor):
    if _sanity_check(k_number):    # and _sanity_check(is_tor):
        join_col = 'mentee_k_number' if is_tor else 'mentor_k_number'
        return _query(f"SELECT k_number, first_name, last_name, gender, year_study, COUNT(Allocation.{join_col}) AS matches FROM Students LEFT JOIN Allocation ON Students.k_number = Allocation.{join_col} WHERE is_mentor != {is_tor} AND k_number != {_to_str(k_number)} GROUP BY Students.k_number ORDER BY matches, k_number ASC;")
    else:
        return "Error: one of the field did not pass the sanity check"

def make_manual_allocation(tee_number, tor_number):
    if _sanity_check(tee_number) and _sanity_check(tor_number):
        return _insert(f"INSERT INTO Allocation VALUES({_to_str(tor_number)}, {_to_str(tee_number)});")
    else:
        return "Error: one of the field did not pass the sanity check"

def remove_allocation(tee_number, tor_number):
    if _sanity_check(tee_number) and _sanity_check(tor_number):
        return _insert(f"DELETE FROM Allocation WHERE mentor_k_number = {_to_str(tor_number)} AND mentee_k_number = {_to_str(tee_number)};")
    else:
        return "Error: one of the field did not pass the sanity check"

def alter_admin_status(k_number, is_admin):
    if _sanity_check(k_number) and _sanity_check(is_admin):
        return _insert(f"UPDATE Students SET is_admin = {is_admin} WHERE k_number = {_to_str(k_number)};")
    else:
        return "Error: one of the field did not pass the sanity check"

if __name__ == '__main__':
    print(_query("SELECT * from Interests;"))
    update_interests("K1543367", ["AI", "ML", "DL"])
    print(_query("SELECT * from Interests;"))
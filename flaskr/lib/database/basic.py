import pymysql, os

# Will set up the credentials
DATABASE_USER = os.environ.get("BUDDY_DB_USER", '')
DATABASE_PASSWORD = os.environ.get("BUDDY_DB_PASSWORD", '')
DB_NAME = "Buddy"
DB_HOST = "buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com"


def query(sql_query):
    """ Returns results of query """
    
    # Connect to the database
    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)

    # Define result
    result = ""   

    try:
    
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

    except Exception as e:
        print("Exeception occured:{}".format(e))

    finally:
        conn.close()

    return result


def insert(sql_query):
    """ Will push a query to the DB"""    

    # Connect to the database
    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)

    # Define result
    result = ""

    try:
        with conn.cursor() as cursor:
            result = cursor.execute(sql_query)

        conn.commit()
            
    except Exception as e:
        print("Exeception occured:{}".format(e))

    finally:
        conn.close()
    
    return result


def sanity_check(sql_fields):
    """ Will sanity check the fields 
        return true, if we can run it"""

    return sql_fields.replace(" ", "").isalnum() or (type(sql_fields) == int)


def to_str(my_str):
    """ Will return the string surrounded by 
        double quotes, useful for SQL query"""

    return "\"" + my_str + "\""


# TODO should I raise my own exception?
def _update_students(**kwargs):
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

        if not sanity_check(value):
            return f"Error: {field} did not pass sanity check"
        elif field not in accepted_fields:
            return f"Error: {field} isn't a column in the table"
        elif type(value) != type(accepted_fields[field]):
            return f"Error: {field} is the wrong type"


    # Ie if there's k_number and another field to update 
    if len(kwargs) > 1:
        sql_query = "UPDATE Students set "
        sql_query += ", ".join([f"{field} = {to_str(value) if type(value)==str else int(value) }" for field, value in kwargs.items() if field != "k_number"])
        sql_query += f" where k_number={to_str(kwargs['k_number'])};" 
    else:
        return "Error: did not pass enough arguments"

    return insert(sql_query)


# TODO check the 0 and 1 return 
def update_students(k_number, first_name=False, last_name=False, degree_title=False, year_study=False, gender=False):
    """ Front end interface of the private function, 
        don't need to know the underlying interface """

    accepted_fields = {"k_number": k_number, "first_name": first_name, "last_name": last_name, "degree_title": degree_title, "year_study": year_study}

    # Set the dictionarry like it's needed
    dict_fields = {field:value for field, value in  accepted_fields.items() if value is not False}

    return _update_students(**dict_fields)


def update_informations():
    pass


def update_mentor():
    pass  


def update_mentee():
    pass
 

def get_user_data(k_number):
    """ Returns all the data in the Students table """
    
    if sanity_check(k_number):
        return query(f"SELECT * FROM Students where k_number={to_str(k_number)};")
    else:
        return "Error: k_number did not pass sanity check"


def get_user_hashed_password(k_number):
    """ Returns the hashed password for the user"""

    if sanity_check(k_number):
        return query(f"select password_hash from Students where k_number={to_str(k_number)};")
    else:
        return "Error: k_number did not pass sanity check"


def get_mentor(mentee_k_number):
    """ Given the mentee K-Number will return its mentor(s) k-number"""

    if sanity_check(mentee_k_number):
        return query(f"SELECT mentor_k_number from Allocation where mentee_k_number={to_str(mentee_k_number)};")
    else:
        return "Error: k_number did not pass sanity check"


def get_mentee(mentor_k_number):
    """ Given the mentor K-Number will return its mentor(s) k-number"""

    if sanity_check(mentor_k_number):
        return query(f"SELECT mentee_k_number from Allocation where mentor_k_number={to_str(mentor_k_number)};")
    else:
        return "Error: k_number did not pass sanity check"



def get_information(k_number):
    """ Given the k_number will return all the extra information on that student"""

    if sanity_check(k_number):
        return query(f"select * from Informations where k_number={to_str(k_number)};")
    else:
        return "Error: the k_number did not pass the sanity check"


def insert_mentor_mentee(mentor_k_number, mentee_k_number):
    """ Insert the mentor, mentee pair k number """

    if sanity_check(mentor_k_number) and sanity_check(mentee_k_number):
        return insert(f"INSERT INTO Allocation VALUES({to_str(mentor_k_number)}, {to_str(mentee_k_number)});")
    else:
        return "Error: one of the k_number did not pass sanity check"


def insert_student():
    pass

def insert_interests(k_number, hobbies, fields):
    """ Will entirely populate an entry for Information table"""
    
    if sanity_check(k_number) and sanity_check(hobbies) and sanity_check(fields):
        return insert(f"INSERT INTO Informations VALUES({to_str(hobbies)}, {to_str(fields)}, {to_str(k_number)});")
    else:
        return "Error: one of the field did not pass the sanity check"

if __name__ == '__main__':

    print(insert("INSERT INTO Students VALUES(\"K1232323\", \"Jean\", \"Dupont\", \"Bsc Robotics\", 1, \"Other\", \"EO(*U&#H@D@#\");"))
    print(query("SELECT * FROM Students;"))
    print(sanity_check("drop Students tables;")) 
    print(_update_students(**{"first_name":"Enzo","test":"test"}))

    print(update_students(k_number="K1631292", first_name="Sacha", degree_title="BA Arts")) 
    print(get_user_data("k1631292"))
    print(get_user_hashed_password("K1631292"))
    print(insert_mentor_mentee("K1631292", "K1232323"))
    print(get_mentor("K1631292"))
    print(get_mentee("K1631292"))

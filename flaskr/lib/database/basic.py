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

    return sql_fields.isalnum() or (type(sql_fields) == int)


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
 
    if len(kwargs) > 1:
        sql_query = "UPDATE Students "
        sql_query += ", ".join([f"set {field} = {to_str(value) if type(value)==str else int(value) }" for field, value in kwargs.items() if field != "k_number"])
        sql_query += f" where k_number={to_str(kwargs['k_number'])};" 
    else:
        return "Error: did not pass enough arguments"

    print(sql_query)

    return query(sql_query)


def update_students(k_number=False, first_name=False, last_name=False, degree_title=False, year_study=False, gender=False):
    """ Front end interface of the private function, 
        don't need to know the underlying interface """

    accepted_fields = {"k_number": k_number, "first_name": first_name, "last_name": last_name, "degree_title": degree_title, "year_study": year_study}

    dict_fields = {field:value for field, value in  accepted_fields.items() if value is not False}

    return _update_students(**dict_fields)
    
if __name__ == '__main__':

    print(insert("INSERT INTO Students VALUES(\"K1232323\", \"Jean\", \"Dupont\", \"Bsc Robotics\", 1, \"Other\", \"EO(*U&#H@D@#\");"))
    print(query("SELECT * FROM Students;"))
    print(sanity_check("drop Students tables;")) 
    print(_update_students(**{"first_name":"Enzo","test":"test"}))

    print(update_students(k_number="K1631292", first_name="Sacha"))

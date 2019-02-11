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

    return sql_fields.isalnum()


def update_students(**kwargs):
    """ Will update fields in Students based on the k_number
        You will need to precise the specific field"""

    accepted_fields = {"first_name":"", "last_name":"", "degree_title":"",
                        "year_study":0, "gender":""}

    
    
    # Need to check that every argument

    # Need to check the type of everything    

   print(k_number) 

if __name__ == '__main__':

    print(insert("INSERT INTO Students VALUES(\"K1232323\", \"Jean\", \"Dupont\", \"Bsc Robotics\", 1, \"Other\", \"EO(*U&#H@D@#\");"))
    print(query("SELECT * FROM Students;"))
    print(sanity_check("drop Students tables;")) 
    print(update_students("K1631292")))

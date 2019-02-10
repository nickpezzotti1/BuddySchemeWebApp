import pymysql

# Will set up the credentials
DATABASE_USER = os.environ.get("BUDDY_DB_USER", '')
DATABASE_PASSWORD = os.environ.get("BUDDY_DB_PASSWORD", '')
DB_NAME = "buddy-scheme"
DB_HOST = "buddy-scheme.cg0eqfj7blbe.eu-west-2.rds.amazonaws.com"


# This is a test function
def connect():
    """ Will connect to the DB"""

    conn = pymysql.connect(DB_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD, db=DB_NAME, connect_timeout=5)
   
    try:
    
        # Select all the users that are in the french society and don't have a ticket yet
        sql_query = "INSERT STUFF"
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

    except Exception as e:
        print("Exeception occured:{}".format(e))

    finally:
        conn.close()

    return "test"

if __name__ == '__main__':

    print("This is a test")

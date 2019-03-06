import pymysql
import boto3
import base64
import json
import logging
from botocore.exceptions import ClientError


class Dao():
    #Ssingleton class to ensure all models use only one DB bridge

    instance = None
    def __init__(self, arg='Buddy'):
        if not Dao.instance:
            Dao.instance = Dao.__Dao(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Dao():
        """ Data access object for database operations"""

        SECRET = "beta/mysql"
        REGION = "eu-west-2"

        def _create_connection(self):
            """ Estabilish database connection """

            try:
                self.__connection = pymysql.connect(
                    host=self._credentials['host'],
                    user = self._credentials['username'],
                    password = self._credentials['password'],
                    db = "clulow_test",   ##self._credentials['dbname'],
                    charset = "utf8mb4",
                    write_timeout = 5,
                    autocommit = True
                )
                self.__cursor = self.__connection.cursor(pymysql.cursors.DictCursor)
                self._log.info("Created DB connection")
            except Exception as e:
                self._log.exception("Could not create DB connection")
                raise

        def execute(self, query):
            """ Execute a provided query and return result"""

            try:
                self.__cursor.execute(query)
                data = self.__cursor.fetchall()
                return data
            except:
                self._log.exception("Could not execute query")
                self.close()
                self._create_connection()
                raise

        def close(self):
            """ Close database connetion """

            try:
                self.__connection.close()
            except:
                self._log.exception("Could not close connection")
                raise

        def commit(self):
            """ Commit created changes """

            try:
                self.__connection.commit()
            except:
                self._log.exception("Could not commit changes")
                raise
        
        def rowcount(self):
            try:
                return self.__cursor.rowcount
            except:
                self._log.exception("Could Not Get Affected Rows")
                raise    
            
        def _get_credentials(self):
            """ Retreive credentials for database connection """

            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=self.REGION
            )

            try:
                get_secret_value_response = client.get_secret_value(
                    SecretId=self.SECRET
                )
            except ClientError as e:
                self._log.exception("Could not retrieve credentials")
                raise e
            else:
                if 'SecretString' in get_secret_value_response:
                    self._credentials = json.loads(get_secret_value_response['SecretString'])
                else:
                    self._credentials = json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))

        def __str__(self):
            return repr(self)

        
        def __init__(self,schema='Buddy'):
            self._log = logging.getLogger(__name__)
            self._schema = schema
            self._get_credentials()
            self._credentials['dbname'] = schema
            self._create_connection()
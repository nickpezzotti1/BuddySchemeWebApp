from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel
import logging

class HobbyModel(BasicModel):

    def delete_hobby(self, hobby_id):
        """ Given the hobby_id will delete the hobby"""

        try:
            self._dao.execute(f"DELETE FROM Hobby WHERE id=hobby_id;")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete the hobby")
            raise e


    def insert_hobby(self, hobby):
        """ Will insert an entry for a hobby into the database"""
        try:
            self._dao.execute(f"INSERT INTO Hobby (hobby_name) VALUES({to_str(hobby)});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the hobby")
            raise e

    def get_hobby_list(self):
        """ Will retrieve a list of possible hobbies from the database"""
        
        try:
            return self._dao.execute(f"SELECT * FROM Hobby;")

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e
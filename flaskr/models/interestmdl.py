from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel
import logging

class InterestModel(BasicModel):

    def delete_interest(self, interest_id):
        """ Given the interest_id will delete the interest"""

        try:
            self._dao.execute(f"DELETE FROM Interest WHERE id=interest_id;")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete the interest")
            raise e


    def insert_interest(self, interest):
        """ Will insert an entry for a interest into the database"""
        try:
            self._dao.execute(f"INSERT INTO Interest (interest_name) VALUES({to_str(interest)});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the interest")
            raise e

    def get_interest_list(self):
        """ Will retrieve a list of possible hobbies from the database"""
        
        try:
            return self._dao.execute(f"SELECT * FROM Interest;")

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e
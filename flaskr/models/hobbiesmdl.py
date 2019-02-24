import dao
from helpers import sanity_check, to_str
from basicmdl import BasicModel
import logging

class HobbiesModel(BasicModel):

    def update_hobbies(self,k_number, hobbies):
        """ Given the k_number and hobbies, will delete all the hobbies
            And reinsert them"""

        if type(hobbies) is not list:
            self._log.exception("Hobbies not passed as list")
            raise TypeError("Hobby/ies must be passed as a list.")

        try:
            delete_hobbies(k_number)

        except Exception as e:
            raise e

        for hobby in hobbies:
            try:
                insert_hobbies(k_number, hobby)

            except Exception as e:
                raise e

        return True


    def get_hobbies(self,k_number):
        """ Given the k_number will return all the student's hobbies"""

        try:
            return self._dao.execute(f"SELECT * FROM Hobbies where k_number={_to_str(k_number)};")

        except Exception as e:
            self._log.exception("Could not get hobbies")
            raise e


    def insert_hobby(self,k_number, hobby):
        """ Will entirely populate an entry for the Hobbies database"""
        try:
            self._dao.execute(f"INSERT INTO Hobbies VALUES({_to_str([hobby, k_number])});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert hobby")
            raise e


    # TODO Need to check for hobbies type
    def delete_hobbies(self,k_number, hobbies=False):
        """ Will delete all the rows where K_number is
             Or only where hobbies and k-number are"""

        if hobbies:
            try:
                self._dao.execute(f"DELETE FROM Hobbies where k_number={_to_str(k_number)} and hobby={_to_str(hobbies)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete single hobby")
                raise e
        else:
            try:
                self._dao.execute(f"DELETE FROM Hobbies where k_number={_to_str(k_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete k_number's hobbies")
                raise e
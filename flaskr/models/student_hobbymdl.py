from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel
import logging

class StudentHobbyModel(BasicModel):

    def get_hobbies(self, scheme_id, k_number):
        """ Given the k_number will return all the student's hobbies"""

        try:
            return self._dao.execute(f"SELECT hobby_id, hobby_name FROM Student_Hobby INNER JOIN Hobby ON Student_Hobby.hobby_id=Hobby.id where k_number={to_str(k_number)} AND scheme_id = {to_str(scheme_id)};")

        except Exception as e:
            self._log.exception("Could not get hobbies")
            raise e

    def insert_hobby(self, k_number, hobby_id):
        """ Will entirely populate an entry for the Hobby database"""
        try:
            self._dao.execute(f"INSERT INTO Student_Hobby VALUES({to_str([hobby_id, k_number])});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert hobby")
            raise e

    def update_hobbies(self, k_number, hobby_ids):
        """ Given the k_number and hobbies, will delete all the hobbies
            And reinsert them"""

        if type(hobby_ids) is not list:
            self._log.exception("Hobbies not passed as list")
            raise TypeError("Hobby/ies must be passed as a list.")

        try:
            self.delete_hobbies(k_number)

        except Exception as e:
            raise e

        for hobby_id in hobby_ids:
            try:
                self.insert_hobby(k_number, hobby_id)

            except Exception as e:
                raise e

        return True

    # TODO Need to check for hobbies type
    def delete_hobbies(self, k_number, hobby=False):
        """ Will delete all the rows where k_number is"""

        if hobby:
            try:
                # TODO Allow for single hobby
                self._dao.execute(f"DELETE Student_Hobby FROM Student_Hobby INNER JOIN Hobby ON Student_Hobby.hobby_id=Hobby.id where k_number={to_str(k_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete single hobby")
                raise e
        else:
            try:
                self._dao.execute(f"DELETE Student_Hobby FROM Student_Hobby INNER JOIN Hobby ON Student_Hobby.hobby_id=Hobby.id where k_number={to_str(k_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete k_number's hobbies")
                raise e
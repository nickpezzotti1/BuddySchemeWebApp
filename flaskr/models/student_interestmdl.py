from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel

class StudentInterestModel(BasicModel):

    def get_interests(self, scheme_id, k_number):
        """ Given the k_number will return all the student's interests"""

        try:
            return self._dao.execute(f"SELECT interest_id, interest_name FROM Student_Interest INNER JOIN Interest ON Student_Interest.interest_id=Interest.id where k_number={to_str(k_number)} AND scheme_id = {to_str(scheme_id)}")

        except Exception as e:
            self._log.exception("Could not get interests")
            raise e

    def insert_interest(self, scheme_id, k_number, interest_id):
        """ Will entirely populate an entry for Student_Interest table"""
        try:
            self._dao.execute(f"INSERT INTO Student_Interest VALUES({to_str([scheme_id, interest_id, k_number])});")
            self._dao.commit()

        except Exception as e:
            raise e

    def update_interests(self, scheme_id, k_number, interest_ids):
        """ Given the k-number of the students and new interests
            Will replace all the interests by the new one"""

        if type(interest_ids) is not list:
            raise TypeError("Interest/s must be passed as a list")

        try:
            self.delete_interests(scheme_id, k_number)

        except Exception as e:
            raise e

        for interest_id in interest_ids:
            try:
                self.insert_interest(scheme_id, k_number, interest_id)

            except Exception as e:
                raise e

        return True

    def delete_interests(self, scheme_id, k_number, interest=False):
        """ Will delete all the rows where the k-number is """

        if interest:
            try:
                # TODO Allow for single interest
                self._dao.execute(f"DELETE Student_Interest FROM Student_Interest INNER JOIN Interest ON Student_Interest.interest_id=Interest.id where k_number={to_str(k_number)} AND scheme_id = {to_str(scheme_id)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete single interest")
                raise e
        else:
            try:
                self._dao.execute(f"DELETE Student_Interest FROM Student_Interest INNER JOIN Interest ON Student_Interest.interest_id=Interest.id where k_number={to_str(k_number)} AND scheme_id = {to_str(scheme_id)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete k_number's interests")
                raise e
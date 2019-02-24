import dao
from helpers import sanity_check, to_str
from basicmdl import BasicModel

class InterestModel(BasicModel):

    def delete_interests(self,k_number, interests=False):
        """ Will delete all the rows where the k-number is """

        if interests:
            try:
                self._dao.execute(f"DELETE FROM Interests where k_number={to_str(k_number)} and interest={to_str(interests)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete single interest")
                raise e
        else:
            try:
                self._dao.execute(f"DELETE FROM Interests where k_number={to_str(k_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete k_number's interests")
                raise e

    def update_interests(self,k_number, interests):
        """ Given the k-number of the students and new interests
            Will replace all the interests by the new one"""

        if type(interests) is not list:
            raise TypeError("Interest/s must be passed as a list")

        try:
            delete_interests(k_number)

        except Exception as e:
            raise e

        for interest in interests:
            try:
                insert_interests(k_number, interest)

            except Exception as e:
                raise e

        return True

    def get_interests(self,k_number):
        """ Given the k_number will return all the student's interests"""

        try:
            return self._dao.execute(f"SELECT * FROM Interests where k_number={to_str(k_number)}")

        except Exception as e:
            self._log.exception("Could not get interests")
            raise e


    def insert_interest(self,k_number, interest):
        """ Will entirely populate an entry for Interests table"""
        try:
            self._dao.execute(f"INSERT INTO Interests VALUES({to_str([interest, k_number])});")
            self._dao.commit()

        except Exception as e:
            raise e
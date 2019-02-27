from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel
import logging

class AllocationModel(BasicModel):

    def update_mentee(self,mentor_k_number, mentees_k_number):
        """ Given the mentor_k_number will update all his mentees"""

        if type(mentees_k_number) is not list:
            self._log.exception("Mentees not passed as list")
            raise TypeError("Mentee/s must be passed as a list.")

        try:
            delete_mentees(mentor_k_number)
        except Exception as e:
                self._log.exception("Could not delete mentees while updating")
                raise e
                return False

        for mentee_k_number in mentees_k_number:
            try:
                insert_mentor_mentee(mentor_k_number, mentee_k_number)
            except Exception as e:
                self._log.exception("Could not insert pair while updating mentee")
                raise e
                return False

        return True


    def update_mentor(self,mentee_k_number, mentors_k_number):
        """ Given the mentee_k_number will update all his mentors"""

        if type(mentors_k_number) is not list:
            self._log.exception("Mentors not passed as list")
            raise TypeError("Mentor/s must be passed as a list.")
        try:
            delete_mentors(mentee_k_number)
        except Exception as e:
                self._log.exception("Could not delete mentors while updating")
                raise e
                return False

        for mentor_k_number in mentors_k_number:
            try:
                insert_mentor_mentee(mentor_k_number, mentee_k_number)
            except Exception as e:
                self._log.exception("Could not insert pairs while updating mentor")
                raise e
                return False

        return True

    def get_all_mentors(self):
        """ Returns all the k-number of mentors"""

        try:
            return self._dao.execute("SELECT mentor_k_number FROM Allocation;")

        except Exception as e:
                self._log.exception("Could not get all mentors")
                raise e


    def get_all_mentees(self):
        """ Returns all the k-number of the mentees"""

        try:
            return self._dao.execute("SELECT mentee_k_number FROM Allocation;")

        except Exception as e:
                self._log.exception("Could not get all mentees")
                raise e


    def get_mentee_details(self,k_number):
        if sanity_check(k_number):

            try:
                return self._dao.execute(f"SELECT k_number, first_name, last_name, year_study FROM Students, Allocation WHERE Students.k_number = Allocation.mentee_k_number AND Allocation.mentor_k_number = {to_str(k_number)};")
        
            except Exception as e:
                self._log.exception("Could not get mentee details")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def get_mentor_details(self,k_number):
        if sanity_check(k_number):

            try:
                return self._dao.execute(f"SELECT k_number, first_name, last_name, year_study FROM Students, Allocation WHERE Students.k_number = Allocation.mentor_k_number AND Allocation.mentee_k_number = {to_str(k_number)};")
        
            except Exception as e:
                self._log.exception("Could not get mentor details")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def get_manual_allocation_matches(self,k_number, is_tor):
        if sanity_check(k_number):    # and _sanity_check(is_tor):
            join_col = 'mentee_k_number' if is_tor else 'mentor_k_number'
            try:
                return self._dao.execute(f"SELECT k_number, first_name, last_name, gender, year_study, COUNT(Allocation.{join_col}) AS matches FROM Students LEFT JOIN Allocation ON Students.k_number = Allocation.{join_col} WHERE is_mentor != {is_tor} AND k_number != {to_str(k_number)} GROUP BY Students.k_number ORDER BY matches, k_number ASC;")
            
            except Exception as e:
                self._log.exception("Could not get manual allocation matches")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def make_manual_allocation(self,tee_number, tor_number):
        if sanity_check(tee_number) and sanity_check(tor_number):
            print(f"INSERT INTO Allocation VALUES({to_str(tor_number)}, {to_str(tee_number)});")
            try:
                return self._dao.execute(f"INSERT INTO Allocation VALUES({to_str(tor_number)}, {to_str(tee_number)});")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not make manual allocation")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def remove_allocation(self,tee_number, tor_number):
        if sanity_check(tee_number) and sanity_check(tor_number):

            try:
                return self._dao.execute(f"DELETE FROM Allocation WHERE mentor_k_number = {to_str(tor_number)} AND mentee_k_number = {to_str(tee_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not remove allocation")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def get_mentors(self,mentee_k_number):
        """ Given the mentee K-Number will return its mentor(s) k-number"""
        
        try:
            return self._dao.execute(f"SELECT mentor_k_number from Allocation where mentee_k_number={to_str(mentee_k_number)};")

        except Exception as e:
            self._log.exception("Could not get mentors")
            raise e

    def get_mentees(self,mentor_k_number):
        """ Given the mentor K-Number will return its mentor(s) k-number"""

        try:
            return self._dao.execute(f"SELECT mentee_k_number from Allocation where mentor_k_number={to_str(mentor_k_number)};")

        except Exception as e:
            self._log.exception("Could not get mentees")
            raise e


    def insert_mentor_mentee(self,mentor_k_number, mentee_k_number):
        """ Insert the mentor, mentee pair k number """

        try:
            self._dao.execute(f"INSERT INTO Allocation VALUES({to_str([mentor_k_number, mentee_k_number])});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not inset mentor mentee pair")
            raise e

    def delete_mentors(self,mentee_k_number):
        """ Given the mentee k-number will delete all his mentors"""
        try:
            self._dao.execute(f"DELETE FROM Allocation where mentee_k_number={to_str(mentee_k_number)};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not get delete mentors")
            raise e

    def delete_mentees(self,mentor_k_number):
        """ Given the mentor k-number will delete all his mentees"""
        try:
            self._dao.execute(f"DELETE FROM Allocation where mentor_k_number={to_str(mentor_k_number)};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete mentees")
            raise e
from flaskr.models.helpers import sanity_check
from flaskr.models.basicmdl import BasicModel


class AllocationModel(BasicModel):

    def update_mentee(self, scheme_id, mentor_k_number, mentees_k_number):
        """ Given the mentor_k_number will update all his mentees"""

        if type(mentees_k_number) is not list:
            self._log.exception("Mentees not passed as list")
            return abort(500)

        try:
            delete_mentees(mentor_k_number)
        except Exception as e:
            self._log.exception("Could not delete mentees while updating")
            return abort(500)

        for mentee_k_number in mentees_k_number:
            try:
                insert_mentor_mentee(mentor_k_number, mentee_k_number)
            except Exception as e:
                self._log.exception("Could not insert pair while updating mentee")
                return abort(500)

        return True

    def update_mentor(self, scheme_id, mentee_k_number, mentors_k_number):
        """ Given the mentee_k_number will update all his mentors"""

        if type(mentors_k_number) is not list:
            self._log.exception("Mentors not passed as list")
            return abort(500)
        try:
            delete_mentors(scheme_id, mentee_k_number)
        except Exception as e:
            self._log.exception("Could not delete mentors while updating")
            return abort(500)

        for mentor_k_number in mentors_k_number:
            try:
                insert_mentor_mentee(scheme_id, mentor_k_number, mentee_k_number)
            except Exception as e:
                self._log.exception("Could not insert pairs while updating mentor")
                return abort(500)

        return True

    def get_all_mentors(self, scheme_id):
        """ Returns all the k-number of mentors"""

        try:
            return self._dao.execute("SELECT k_number, gender, buddy_limit, date_of_birth FROM Student WHERE is_mentor=1 AND scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get all mentors")
            return abort(500)

    def get_all_mentees(self, scheme_id):
        """ Returns all the k-number of the mentees"""

        try:
            return self._dao.execute("SELECT k_number, gender, buddy_limit, date_of_birth FROM Student WHERE is_mentor = 0 AND scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get all mentees")
            return abort(500)

    def get_mentee_details(self, scheme_id, k_number):
        if sanity_check(k_number):

            try:
                return self._dao.execute("SELECT k_number, first_name, last_name, year_study FROM Student, Allocation WHERE Student.k_number = Allocation.mentee_k_number AND Allocation.mentor_k_number = %s AND Student.scheme_id = %s;", (k_number, scheme_id))

            except Exception as e:
                self._log.exception("Could not get mentee details")
                raise e

        else:
            return abort(500)

    def get_mentor_details(self, scheme_id, k_number):
        if sanity_check(k_number):

            try:
                return self._dao.execute("SELECT k_number, first_name, last_name, year_study FROM Student, Allocation WHERE Student.k_number = Allocation.mentor_k_number AND Allocation.mentee_k_number = %s AND Student.scheme_id = %s;", (k_number, scheme_id))

            except Exception as e:
                self._log.exception("Could not get mentor details")
                raise e

        else:
            return abort(500)

    def get_manual_allocation_matches(self, scheme_id, k_number, is_tor):
        if sanity_check(k_number):    # and _sanity_check(is_tor):
            join_col = 'mentee_k_number' if is_tor else 'mentor_k_number'
            other_col = 'mentee_k_number' if not is_tor else 'mentor_k_number'
            try:
                return self._dao.execute(f"SELECT * FROM (SELECT k_number, first_name, last_name, gender, year_study, COUNT(Allocation.{join_col}) AS matches FROM Student LEFT JOIN Allocation ON Student.k_number = Allocation.{join_col} AND Student.scheme_id = Allocation.scheme_id WHERE is_mentor != %s AND k_number != %s AND Student.scheme_id = %s GROUP BY Student.k_number ORDER BY matches, k_number ASC) AS matches WHERE NOT EXISTS (SELECT NULL FROM Allocation WHERE {other_col} = %s AND {join_col} = matches.k_number AND scheme_id = %s);", (is_tor, k_number, scheme_id, k_number, scheme_id))

            except Exception as e:
                self._log.exception("Could not get manual allocation matches")
                raise e

        else:
            return abort(500)

    def make_manual_allocation(self, scheme_id, tee_number, tor_number):
        if sanity_check(tee_number) and sanity_check(tor_number):

            try:
                return self._dao.execute("INSERT INTO Allocation VALUES(%s, %s, %s);", (scheme_id, tor_number, tee_number))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not make manual allocation")
                raise e

        else:
            return abort(500)

    def remove_allocation(self, scheme_id, tee_number, tor_number):
        if sanity_check(tee_number) and sanity_check(tor_number):

            try:
                return self._dao.execute("DELETE FROM Allocation WHERE mentor_k_number = %s AND mentee_k_number = %s AND scheme_id = %s;", (tor_number, tee_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not remove allocation")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def get_mentors(self, scheme_id, mentee_k_number):
        """ Given the mentee K-Number will return its mentor(s) k-number"""

        try:
            return self._dao.execute("SELECT mentor_k_number from Allocation where mentee_k_number= %s AND scheme_id = %s;", (mentee_k_number, scheme_id))

        except Exception as e:
            self._log.exception("Could not get mentors")
            raise e

    def get_mentees(self, scheme_id, mentor_k_number):
        """ Given the mentor K-Number will return its mentor(s) k-number"""

        try:
            return self._dao.execute(f"SELECT mentee_k_number from Allocation where mentor_k_number = %s AND scheme_id = %s;", (mentor_k_number, scheme_id))

        except Exception as e:
            self._log.exception("Could not get mentees")
            raise e

    def insert_mentor_mentee(self, scheme_id, mentor_k_number, mentee_k_number):
        """ Insert the mentor, mentee pair k number """

        try:
            self._dao.execute("INSERT INTO Allocation VALUES(%s, %s, %s);",
                              (scheme_id, mentor_k_number, mentee_k_number))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not inset mentor mentee pair")
            raise e

    def delete_mentors(self, scheme_id, mentee_k_number):
        """ Given the mentee k-number will delete all his mentors"""
        try:
            self._dao.execute(
                "DELETE FROM Allocation where mentee_k_number = %s AND scheme_id = %s;", (mentee_k_number, scheme_id))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not get delete mentors")
            raise e

    def delete_mentees(self, scheme_id, mentor_k_number):
        """ Given the mentor k-number will delete all his mentees"""
        try:
            self._dao.execute(
                "DELETE FROM Allocation where mentor_k_number = %s AND scheme_id = %s;", (mentor_k_number, scheme_id))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete mentees")
            raise e

    def clear_allocations_table(self, scheme_id):
        """ Clear all the allocations in the current scheme """
        try:
            self._dao.execute("DELETE FROM Allocation where scheme_id = %s;", (scheme_id, ))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete all the entries in the allocation table")
            raise e

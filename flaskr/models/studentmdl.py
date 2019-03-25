from flaskr.models.basicmdl import BasicModel
from flaskr.models.helpers import sanity_check
from flaskr.models.helpers import to_str


class StudentModel(BasicModel):

    HASH_COL = 'password_hash'

    def _update_students(self, ** kwargs):
        """ Will update fields in Student based on the k_number
            You will need to precise the specific field"""

        accepted_fields = {"scheme_id": int, "first_name": str, "last_name": str, "degree_title": str,
                           "year_study": int, "gender": str, "k_number": str, "is_mentor": bool,
                           "email_confirmed": bool, "is_admin": bool}

        # We need the k_number to update
        if "k_number" not in kwargs:
            raise NameError("K-number could not be found in the list of arguments")

        # Will check that the field is valid, only alphanum and right type
        for field, value in kwargs.items():

            if field not in accepted_fields:
                self._log.exception("Error")
                raise Exception(f"{field} isn't a column in the table")
            elif type(value) != accepted_fields[field]:
                self._log.exception("Error")
                raise TypeError(f"{field} is the wrong type")

        # Ie if there's k_number and another field to update
        if len(kwargs) > 1:
            sql_query = "UPDATE Student set "
            sql_query += ", ".join([f"{field} = {to_str(value)}" for field,
                                    value in kwargs.items() if field != "k_number"])
            sql_query += f" where k_number={to_str(kwargs['k_number'])} AND Student.scheme_id = {to_str(scheme_id)};"
            try:
                self._dao.execute(sql_query)
                self._dao.commit()

            except Exception as e:
                self._log.exception("Error")
                raise e
        else:
            raise Exception("Need at least one argument.")

    def update_students(self, scheme_id, k_number, first_name=[], last_name=[], degree_title=[], year_study=[], gender=[], is_mentor=[], is_admin=[], email_confirmed=[], date_of_birth=[]):
        """ Front end interface of the private function,
            don't need to know the underlying interface """

        accepted_fields = {"scheme_id": scheme_id, "k_number": k_number, "first_name": first_name,
                           "last_name": last_name, "degree_title": degree_title,
                           "year_study": year_study, "gender": gender, "is_mentor": is_mentor,
                           "is_admin": is_admin, "date_of_birth": date_of_birth, "email_confirmed": email_confirmed}

        # Set the dictionarry like it's needed
        dict_fields = {field: value for field,
                       value in accepted_fields.items() if type(value) is not list}

        return self._update_students(** dict_fields)

    def update_hash_password(self, scheme_id, k_number, password_hash):
        """ Given the k_number, will update the password_hash"""

        if type(password_hash) is str:
            try:
                self._dao.execute(
                    "UPDATE Student set password_hash = %s WHERE k_number = %s AND scheme_id = %s;", (password_hash, k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not update hash")
                raise e
        else:
            raise TypeError(f"{type(password_hash)} type isn't accepted")

    def get_user_data(self, scheme_id, k_number):
        """ Returns all the data in the Student table except from password hash"""
        # sanity
        try:
            result = self._dao.execute(
                "SELECT * FROM Student WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))[0]
            result.pop(self.HASH_COL, None)  # can check not none
            return result

        except IndexError:
            raise IndexError(f"{k_number} doesn't exist.")
        except KeyError:
            raise KeyError(f"{self.HASH_COL} not found in table.")

    def user_exist(self, scheme_id, k_number):
        pass

    # TODO Should I return something here?

    def get_user_hashed_password(self, scheme_id, k_number):
        """ Returns the hashed password for the user"""
        # sanity
        try:
            result = self._dao.execute(
                "select password_hash from Student WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            return result[0].pop(self.HASH_COL, None)

        except IndexError:
            raise IndexError(f"{k_number} does not exist.")
        except KeyError:
            raise KeyError(f"{self.HASH_COL} not found in table")

    def insert_student(self, scheme_id, k_number, first_name, last_name, degree_title, year_study, gender, is_mentor, password_hash, is_admin, buddy_limit):
        """ Will entirely populate an entry for Student table"""

        try:
            self._dao.execute("INSERT INTO Student VALUES(%s, %s, %s, %s, %s, %s, %s, %s, FALSE, %s, %s, %s, NULL);", (scheme_id,
                                                                                                                       k_number, first_name, last_name, degree_title, year_study, gender, is_mentor, password_hash, is_admin, buddy_limit))
            succ = self._dao.rowcount()
            self._dao.commit()
            return succ

        except Exception as e:
            self._log.exception("Could not insert student")
            raise e

    def delete_students(self, scheme_id, k_number):
        """ Delete the student entry in the Tables"""
        # sanity?
        try:
            self._dao.execute("DELETE FROM Allocation WHERE mentor_k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            self._dao.execute("DELETE FROM Allocation WHERE mentee_k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            self._dao.execute("DELETE FROM Student_Hobby WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            self._dao.execute("DELETE FROM Student_Interest WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            self._dao.execute("DELETE FROM Student WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
            succ = self._dao.rowcount()
            self._dao.commit()
            return succ

        except Exception as e:
            self._log.exception("Could not delete student")
            raise e

    def get_all_students_data_basic(self, scheme_id):
        if sanity_check(scheme_id):

            try:
                # add has matches
                return self._dao.execute("SELECT k_number, first_name, last_name, gender, is_mentor FROM Student WHERE Student.scheme_id = %s ORDER BY last_name ASC;", (scheme_id,))

            except Exception as e:
                self._log.exception("Could not get all data for a student")
                raise e

    def alter_admin_status(self, scheme_id, k_number, is_admin):
        if sanity_check(scheme_id) and sanity_check(k_number) and sanity_check(is_admin):

            try:
<<<<<<< HEAD
                self._dao.execute(
                    "UPDATE Student SET is_admin = {is_admin} WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
=======
                self._dao.execute("UPDATE Student SET is_admin = %s WHERE k_number = %s AND scheme_id = %s;", (is_admin, k_number, scheme_id))
                succ = self._dao.rowcount()
>>>>>>> dev
                self._dao.commit()
                return succ

            except Exception as e:
                self._log.exception("Could not alter admin status")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def activateAccount(self, scheme_id, k_number):
        if sanity_check(scheme_id) and sanity_check(k_number):

            try:
                self._dao.execute(
                    "UPDATE Student SET email_confirmed = True WHERE WHERE k_number = %s AND scheme_id = %s;", (k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not activate account")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def delete_mentees(self, scheme_id, mentor_k_number):
        """ Given the mentor k-number will delete all his mentees"""
        if sanity_check(scheme_id) and sanity_check(mentor_k_number):
            try:
                self._dao.execute(
                    "DELETE FROM Allocation WHERE mentor_k_number = %s AND scheme_id = %s;", (mentor_k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not delete mentees")
                raise e

    def update_date_of_birth(self, scheme_id, k_number, date_of_birth):
        if sanity_check(scheme_id) and sanity_check(k_number):
            # sanity check dob
            try:
                self._dao.execute(
                    "UPDATE Student SET date_of_birth = %s WHERE k_number = %s AND scheme_id = %s;", (date_of_birth, k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not alter date_of_birth")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def update_gender(self, scheme_id, k_number, gender):
        if sanity_check(scheme_id) and sanity_check(k_number):
            # sanity check dob
            try:
                self._dao.execute(
                    "UPDATE Student SET gender = %s WHERE k_number = %s AND scheme_id = %s;", (gender, k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not alter gender")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def update_buddy_limit(self, scheme_id, k_number, buddy_limit):
        if sanity_check(scheme_id) and sanity_check(k_number):
            # sanity check dob
            try:
                self._dao.execute(
                    "UPDATE Student SET buddy_limit = %s WHERE k_number = %s AND scheme_id = %s;", (buddy_limit, k_number, scheme_id))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not alter buddy_limit")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

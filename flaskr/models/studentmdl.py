import dao
from helpers import sanity_check, to_str
from basicmdl import BasicModel

class StudentModel(BasicModel):

    HASH_COL = 'password_hash'

    def _update_students(self, ** kwargs):
        """ Will update fields in Students based on the k_number
            You will need to precise the specific field"""

        accepted_fields = {"first_name":str, "last_name":str, "degree_title":str,
            "year_study":int, "gender":str, "k_number":str, "is_mentor":bool,
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
            sql_query = "UPDATE Students set "
            sql_query += ", ".join([f"{field} = {_to_str(value)}" for field, value in kwargs.items() if field != "k_number"])
            sql_query += f" where k_number={_to_str(kwargs['k_number'])};"
            try:
                self._dao.execute(sql_query)
                self._dao.commit()

            except Exception as e:
                self._log.exception("Error")
                raise e
        else:
            raise Exception("Need at least one argument.")



    def update_students(self,k_number, first_name=[], last_name=[], degree_title=[], year_study=[], gender=[], is_mentor=[], is_admin=[], email_confirmed=[]):
        """ Front end interface of the private function,
            don't need to know the underlying interface """

        accepted_fields = {"k_number": k_number, "first_name": first_name,
            "last_name": last_name, "degree_title": degree_title,
            "year_study": year_study, "gender": gender, "is_mentor": is_mentor,
            "is_admin": is_admin, "email_confirmed": email_confirmed}

        # Set the dictionarry like it's needed
        dict_fields = {field:value for field, value in  accepted_fields.items() if type(value) is not list}

        return _update_students( ** dict_fields)

    def update_hash_password(self,k_number, password_hash):
        """ Given the k_number, will update the password_hash"""

        if type(password_hash) is str:
            password_hash_sql = "\"" + password_hash + "\""
            try:
                self._dao.execute(f"UPDATE Students set password_hash={password_hash_sql};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not update hash")
                raise e
        else:
            raise TypeError(f"{type(password_hash)} type isn't accepted")


    def get_user_data(self,k_number):
        """ Returns all the data in the Students table except from password hash"""

        try:
            result = self._dao.execute(f"SELECT * FROM Students where k_number={to_str(k_number)};")[0]
            result.pop(self.HASH_COL, None) # can check not none
            return result

        except IndexError:
            raise IndexError(f"{k_number} doesn't exist.")
        except KeyError:
            raise KeyError(f"{self.HASH_COL} not found in table.")

    #TODO Should I return something here?

    def get_user_hashed_password(self,k_number):
        """ Returns the hashed password for the user"""

        try:
            result = self._dao.execute(f"select password_hash from Students where k_number={to_str(k_number)};")
            return result[0].pop(self.HASH_COL, None)

        except IndexError:
            raise IndexError(f"{k_number} does not exist.")
        except KeyError:
            raise KeyError(f"{self.HASH_COL} not found in table")


    def insert_student(self,k_number, first_name, last_name, degree_title, year_study, gender, is_mentor, password_hash, is_admin):
        """ Will entirely populate an entry for Students table"""

        try:
            self._dao.execute(f"INSERT INTO Students VALUES({to_str([k_number, first_name, last_name, degree_title, year_study, gender, is_mentor])}, FALSE, {_to_str(password_hash, password_hash=True)}, {_to_str(is_admin)});")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert student")
            raise e

    def delete_students(self,k_number):
        """ Delete the students entry in the Tables"""

        try:
            self._dao.execute(f"DELETE FROM Students where k_number={to_str(k_number)};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete student")
            raise e


    def get_all_students_data_basic(self):

        try:
            return self._dao.execute("SELECT k_number, first_name, last_name, gender, is_mentor FROM Students ORDER BY last_name ASC;")   ## add has matches

        except Exception as e:
            self._log.exception("Could not get all data for a student")
            raise e



    def alter_admin_status(self,k_number, is_admin):
        if sanity_check(k_number) and sanity_check(is_admin):

            try:
                self._dao.execute(f"UPDATE Students SET is_admin = {is_admin} WHERE k_number = {_to_str(k_number)};")
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not alter admin status")
                raise e

        else:
            return "Error: one of the field did not pass the sanity check"

    def delete_mentees(self,mentor_k_number):
        """ Given the mentor k-number will delete all his mentees"""
        try:
            self._dao.execute(f"DELETE FROM Allocation where mentor_k_number={_to_str(mentor_k_number)};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete mentees")
            raise e
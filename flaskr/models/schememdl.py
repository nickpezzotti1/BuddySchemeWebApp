from flaskr.models.basicmdl import BasicModel
from flaskr.models.helpers import sanity_check
from flaskr.models.helpers import to_str


class SchemeModel(BasicModel):

    ## This should not be in this model
    def get_system_admin_pass(self, email):
        try:
            return self._dao.execute("SELECT password_hash FROM Super_user WHERE email = %s;", (email, ))[0]['password_hash']

        except Exception as e:
            self._log.exception("Could Get System Admin Password")
            raise e

    def get_all_scheme_data(self):
        try:
            return self._dao.execute("SELECT Scheme.scheme_id, scheme_name, is_active, COUNT(Student.scheme_id) as student_count FROM Scheme LEFT JOIN Student ON Scheme.scheme_id = Student.scheme_id GROUP BY Scheme.scheme_id ORDER BY Scheme.is_active DESC, Scheme.scheme_name ASC;")

        except Exception as e:
            self._log.exception("Could Not Get Scheme Data")
            raise e

    def update_hash_password(self, email, password_hash):
        """ Given the email, will update the password_hash """

        if type(password_hash) is str:
            try:
                self._dao.execute(
                    "UPDATE Super_user set password_hash = %s WHERE email = %s;", (password_hash, email))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could not update hash")
                raise e
        else:       
            raise TypeError(f"{type(password_hash)} type isn't accepted")

    def get_active_scheme_data(self):
        try:
            return self._dao.execute("SELECT scheme_id, scheme_name FROM Scheme WHERE is_active = 1;")

        except Exception as e:
            self._log.exception("Could Not Get Acitve Scheme Data")
            raise e

    def check_scheme_avail(self, scheme_name):
        """Returns true if new scheme name is available"""
        if True:  # sanity_check(scheme_name):
            try:
                return self._dao.execute("SELECT IF (COUNT(scheme_name) > 0, false, true) AS avail FROM Scheme WHERE scheme_name = %s;", (scheme_name, ))[0]['avail']

            except Exception as e:
                self._log.exception("Could Not Confirm Scheme Name Is Available")
                raise e

    def create_new_scheme(self, scheme_name):
        """Inserts a new scheme"""
        try:
            self._dao.execute("INSERT INTO Scheme VALUES(0, %s, 1);", (scheme_name, ))
            succ = self._dao.rowcount()
            self._dao.commit()
            return succ

        except Exception as e:
            self._log.exception("Could Not Create New Scheme")
            raise e

    ## This should not be in this model
    def create_allocation_config_entry(self, scheme_id):
        """Inserts an entry for new scheme into allocation_config"""
        if sanity_check(scheme_id):  
            try:
                self._dao.execute("INSERT INTO Allocation_Config VALUES(%s, 1, 10, 5, 5, 0);", (scheme_id, ))
                succ = self._dao.rowcount()
                self._dao.commit()
                return succ

            except Exception as e:
                self._log.exception("Could Not Create New Scheme")
                raise e

    def get_scheme_id(self, scheme_name):
        """Returns true if new scheme name is available"""
        if True:  # sanity_check(scheme_name):
            try:
                # errors if not exists
                return self._dao.execute("SELECT scheme_id FROM Scheme WHERE scheme_name = %s;", (scheme_name, ))[0]['scheme_id']

            except Exception as e:
                self._log.exception("Could Not Get Scheme ID")
                raise e

    ## Why is there a case here
    def suspend_scheme(self, scheme_id):
        """Suspends a given scheme"""
        if sanity_check(scheme_id):
            try:
                self._dao.execute(
                    "UPDATE Scheme SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END WHERE scheme_id = %s;", (scheme_id, ))
                self._dao.commit()

            except Exception as e:
                self._log.exception("Could Not suspend scheme")
                raise e

    def delete_scheme(self, scheme_id):
        """Suspends a given scheme"""
        if sanity_check(scheme_id):
            try:
                self._dao.execute("DELETE FROM Scheme WHERE scheme_id = %s;",
                                  (scheme_id, )) 
                succ = self._dao.rowcount()
                self._dao.commit()
                return succ

            except Exception as e:
                self._log.exception("Could Not delete scheme")
                raise e

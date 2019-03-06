from models.basicmdl import BasicModel
from models.helpers import sanity_check
from models.helpers import to_str

class SchemeModel(BasicModel):

    def get_system_admin_pass(self, email):
        ## sanity but needs @ symbol
        try:
            return self._dao.execute(f"SELECT password_hash FROM Super_user WHERE email = {to_str(email)};")[0]['password_hash'] ## won't work needs @
            
        except Exception as e:
            self._log.exception("Could Get System Admin Password")
            raise e
        
    def get_all_scheme_data(self):
        try:
            return self._dao.execute("SELECT Scheme.scheme_id, scheme_name, is_active, COUNT(Student.scheme_id) as student_count FROM Scheme LEFT JOIN Student ON Scheme.scheme_id = Student.scheme_id GROUP BY Scheme.scheme_id ORDER BY Scheme.is_active DESC, Scheme.scheme_name ASC;")
            
        except Exception as e:
            self._log.exception("Could Not Get Scheme Data")
            raise e
        
    def get_active_scheme_data(self):
        try:
            return self._dao.execute("SELECT scheme_id, scheme_name FROM Scheme WHERE is_active = 1;") 
        
        except Exception as e:
            self._log.exception("Could Not Get Acitve Scheme Data")
            raise e
    
    def check_scheme_avail(self, scheme_name):
        """Returns true if new scheme name is available"""
        if sanity_check(scheme_name):
            try:
                return self._dao.execute(f"SELECT IF (COUNT(scheme_name) > 0, false, true) AS avail FROM Scheme WHERE scheme_name = {to_str(scheme_name)};")[0]['avail']
            
            except Exception as e:
                self._log.exception("Could Not Confirm Scheme Name Is Available")
                raise e
        
    def create_new_scheme(self, scheme_name, is_active=1):
        """Inserts a new scheme"""
        if sanity_check(scheme_name) and sanity_check(is_active):  ## combine check and add ?
            try:
                self._dao.execute(f"INSERT INTO Scheme VALUES(0, {to_str(scheme_name)}, {to_str(is_active)});") 
                succ = self._dao.rowcount()
                self._dao.commit()
                return succ
                
            except Exception as e:
                self._log.exception("Could Not Create New Scheme")
                raise e
    
    def get_scheme_id(self, scheme_name):
        """Returns true if new scheme name is available"""
        if sanity_check(scheme_name):
            try:
                res = self._dao.execute(f"SELECT scheme_id FROM Scheme WHERE scheme_name = {to_str(scheme_name)};")[0]['scheme_id'] ## errors if not exists
            
            except Exception as e:
                self._log.exception("Could Not Get Scheme ID")
                raise e
            
    def suspend_scheme(self, scheme_id):        
        """Suspends a given scheme"""
        if sanity_check(scheme_id):
            try:
                self._dao.execute(f"UPDATE Scheme SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END WHERE scheme_id = {to_str(scheme_id)};")
                self._dao.commit()
            
            except Exception as e:
                self._log.exception("Could Not Get Scheme ID")
                raise e
            
    def delete_scheme(self, scheme_id):        
        """Suspends a given scheme"""
        if sanity_check(scheme_id):
            try:
                self._dao.execute(f"DELETE FROM Scheme WHERE scheme_id = {to_str(scheme_id)};") ## needs cascades
                self._dao.commit()
            
            except Exception as e:
                self._log.exception("Could Not Get Scheme ID")
                raise e
            
   
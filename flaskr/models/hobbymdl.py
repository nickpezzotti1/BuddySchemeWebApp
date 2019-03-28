from flaskr.models.basicmdl import BasicModel


class HobbyModel(BasicModel):

    def delete_hobby(self, scheme_id, hobby_id):
        """ Given the hobby_id will delete the hobby"""

        try:
            self._dao.execute("DELETE FROM Hobby WHERE id = %s AND scheme_id = %s;", (hobby_id, scheme_id))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete the hobby")
            raise e

    def insert_hobby(self, scheme_id, hobby):
        """ Will insert an entry for a hobby into the database"""
        try:
            self._dao.execute("INSERT INTO Hobby (scheme_id, hobby_name) VALUES(%s, %s);", (scheme_id, hobby))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the hobby")
            raise e

    def select_hobby(self, scheme_id, hobby):
        """ Will select a hobby from the database"""
        try:
           return self._dao.execute(
                "SELECT * FROM Hobby WHERE scheme_id = %s AND hobby_name = %s;", (scheme_id, hobby))

        except Exception as e:
            self._log.exception("Could not select the hobby")
            raise e

    def get_hobby_list(self, scheme_id):  
        """ Will retrieve a list of possible hobbies from the database"""

        try:
            return self._dao.execute("SELECT * FROM Hobby WHERE scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e

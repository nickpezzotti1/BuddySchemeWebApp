from flaskr.models.basicmdl import BasicModel


class HobbyModel(BasicModel):

    def delete_hobby(self, hobby_id, scheme_id=1):  # add scheme id
        """ Given the hobby_id will delete the hobby"""

        try:
            self._dao.execute("DELETE FROM Hobby WHERE id = %s AND scheme_id = %s;",
                              (hobby_id, scheme_id))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not delete the hobby")
            raise e

    def insert_hobby(self, hobby, scheme_id=1):
        """ Will insert an entry for a hobby into the database"""
        try:
            self._dao.execute("INSERT INTO Hobby (hobby_name) VALUES(%s);", (hobby, )) ##, %s);", (scheme_id, hobby))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the hobby")
            raise e

    def get_hobby_list(self, scheme_id=1):  # add scheme_id
        """ Will retrieve a list of possible hobbies from the database"""

        try:
            return self._dao.execute("SELECT * FROM Hobby;") ## WHERE scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e

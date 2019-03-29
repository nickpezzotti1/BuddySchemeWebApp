from flaskr.models.basicmdl import BasicModel


class InterestModel(BasicModel):

    def delete_interest(self, scheme_id, interest_id):
        """ Given the interest_id will delete the interest"""

        try:
            self._dao.execute("DELETE FROM Interest WHERE id = %s AND scheme_id = %s;", (interest_id, scheme_id))
            succ = self._dao.rowcount()
            self._dao.commit()
            return succ

        except Exception as e:
            self._log.exception("Could not delete the interest")
            raise e

    def insert_interest(self, scheme_id, interest):
        """ Will insert an entry for a interest into the database"""
        try:
            self._dao.execute(
                "INSERT INTO Interest (scheme_id, interest_name) VALUES(%s, %s);", (scheme_id, interest))
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not insert the interest")
            raise e

    def get_interest_list(self, scheme_id):
        """ Will retrieve a list of possible hobbies from the database"""

        try:
            return self._dao.execute("SELECT * FROM Interest WHERE scheme_id = %s;", (scheme_id, ))

        except Exception as e:
            self._log.exception("Could not get the list of hobbies")
            raise e

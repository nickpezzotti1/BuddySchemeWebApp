import models.dao as dao
import logging

class BasicModel:

    def __init__(self, schema='jardin_test'):
        try:
            self._dao = dao.Dao(schema)
            self._log = logging.getLogger(__name__)
        except Exception as e:
                self._log.exception("Could not initiate model")
                raise e
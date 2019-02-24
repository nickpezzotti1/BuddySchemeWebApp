import dao
import logging

class BasicModel:

	def __init__(self):
	        self._dao = dao.Dao()
	        self._log = logging.getLogger(__name__)
from models.helpers import sanity_check, to_str
from models.basicmdl import BasicModel
import logging

class AllocationConfigModel(BasicModel):

    def get_allocation_config(self):
        """ Retrieve the current allocation configuration"""

        try:
            return self._dao.execute("SELECT age_weight, gender_weight, hobby_weight, interest_weight FROM Allocation_Config;")

        except Exception as e:
            self._log.exception("Could not get allocation config")
            raise e

    def update_allocation_config(self, config):
        """ Update the allocation configuration table with the new """
        
        # Sanity check all config fields
        for config_field, config_value in config.items():
            if not sanity_check(config_value):
                return "Error: one of the field did not pass the sanity check"

        try:
            self._dao.execute(f"UPDATE Allocation_Config SET age_weight = {config['age_weight']}, gender_weight = {config['gender_weight']}, hobby_weight = {config['hobby_weight']}, interest_weight = {config['interest_weight']};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not update allocation config")
            raise e

        
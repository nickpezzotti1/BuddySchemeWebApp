from flaskr.models.helpers import sanity_check, to_str
from flaskr.models.basicmdl import BasicModel
import logging

class AllocationConfigModel(BasicModel):

    def get_allocation_config(self, scheme_id):
        """ Retrieve the current allocation configuration"""
        if sanity_check(scheme_id):
            try:
                return self._dao.execute(f"SELECT age_weight, gender_weight, hobby_weight, interest_weight FROM Allocation_Config WHERE scheme_id = {to_str(scheme_id)};")[0]

            except Exception as e:
                self._log.exception("Could not get allocation config")
                return abort(500)

    def update_allocation_config(self, scheme_id, config):
        """ Update the allocation configuration table with the new """

        # Sanity check all config fields
        for config_field, config_value in config.items():
            if not sanity_check(config_value) and sanity_check(scheme_id):
                return "Error: one of the field did not pass the sanity check"

        try:
            self._dao.execute(f"UPDATE Allocation_Config SET age_weight = {config['age_weight']}, gender_weight = {config['gender_weight']}, hobby_weight = {config['hobby_weight']}, interest_weight = {config['interest_weight']} WHERE scheme_id = {to_str(scheme_id)};")
            self._dao.commit()

        except Exception as e:
            self._log.exception("Could not update allocation config")
            return abort(500)

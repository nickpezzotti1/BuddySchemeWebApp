from werkzeug.exceptions import abort

from flaskr.models.helpers import sanity_check, to_str
from flaskr.models.basicmdl import BasicModel


class AllocationConfigModel(BasicModel):

    def get_allocation_config(self, scheme_id):
        """ Retrieve the current allocation configuration"""
        if sanity_check(scheme_id):
            pass

    def update_allocation_config(self, scheme_id, config):
        """ Update the allocation configuration table with the new """

        # Sanity check all config fields
        for config_field, config_value in config.items():
            if not sanity_check(config_value) and sanity_check(scheme_id):
                return "Error: one of the field did not pass the sanity check"

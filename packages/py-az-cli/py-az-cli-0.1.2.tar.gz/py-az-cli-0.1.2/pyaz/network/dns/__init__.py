from ... pyaz_utils import call_az
from . import record_set, zone


def list_references(parameters):
    return call_az("az network dns list-references", locals())


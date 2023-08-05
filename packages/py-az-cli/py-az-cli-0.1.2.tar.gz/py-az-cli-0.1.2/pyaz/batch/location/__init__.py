from ... pyaz_utils import call_az
from . import quotas


def list_skus(location, filter=None, maxresults=None):
    '''
    List virtual machine SKUs available in a location.
    '''
    return call_az("az batch location list-skus", locals())


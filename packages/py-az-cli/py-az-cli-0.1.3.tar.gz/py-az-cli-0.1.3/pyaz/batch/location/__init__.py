from ... pyaz_utils import _call_az
from . import quotas


def list_skus(location, filter=None, maxresults=None):
    '''
    List virtual machine SKUs available in a location.
    '''
    return _call_az("az batch location list-skus", locals())


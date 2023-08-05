from ... pyaz_utils import call_az
from . import group, mg, sub, tenant


def list(name):
    '''
    List deployment operations at subscription scope.
    '''
    return call_az("az deployment operation list", locals())


def show(name, operation_ids):
    '''
    Show a deployment operation at subscription scope.
    '''
    return call_az("az deployment operation show", locals())


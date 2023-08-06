from ... pyaz_utils import _call_az

def list():
    '''
    Get operations from all providers.
    '''
    return _call_az("az provider operation list", locals())


def show(namespace):
    '''
    Get an individual provider's operations.
    '''
    return _call_az("az provider operation show", locals())


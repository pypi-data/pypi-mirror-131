from ... pyaz_utils import call_az

def list():
    '''
    Get operations from all providers.
    '''
    return call_az("az provider operation list", locals())


def show(namespace):
    '''
    Get an individual provider's operations.
    '''
    return call_az("az provider operation show", locals())


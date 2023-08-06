from .... pyaz_utils import _call_az

def list(name):
    '''
    List deployment operations at tenant scope.
    '''
    return _call_az("az deployment operation tenant list", locals())


def show(name, operation_ids):
    '''
    Show a deployment operation at tenant scope.
    '''
    return _call_az("az deployment operation tenant show", locals())


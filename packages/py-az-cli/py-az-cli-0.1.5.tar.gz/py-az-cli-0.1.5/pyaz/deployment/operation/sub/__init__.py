from .... pyaz_utils import _call_az

def list(name):
    '''
    List deployment operations at subscription scope.
    '''
    return _call_az("az deployment operation sub list", locals())


def show(name, operation_ids):
    '''
    Show a deployment operation at subscription scope.
    '''
    return _call_az("az deployment operation sub show", locals())


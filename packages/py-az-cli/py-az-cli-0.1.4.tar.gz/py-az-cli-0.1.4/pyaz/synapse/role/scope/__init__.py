from .... pyaz_utils import _call_az

def list(workspace_name):
    '''
    List role scopes.
    '''
    return _call_az("az synapse role scope list", locals())


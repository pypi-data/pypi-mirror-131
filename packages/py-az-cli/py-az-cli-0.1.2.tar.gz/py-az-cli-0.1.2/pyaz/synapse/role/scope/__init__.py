from .... pyaz_utils import call_az

def list(workspace_name):
    '''
    List role scopes.
    '''
    return call_az("az synapse role scope list", locals())


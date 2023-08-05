from .... pyaz_utils import call_az

def list(workspace_name, is_built_in=None):
    '''
    List role definitions.
    '''
    return call_az("az synapse role definition list", locals())


def show(role, workspace_name):
    '''
    Get role definition by role id/name.
    '''
    return call_az("az synapse role definition show", locals())


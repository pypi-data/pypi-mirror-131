from ... pyaz_utils import _call_az

def list(name, resource_group=None):
    '''
    List the deployment token for the static app.
    '''
    return _call_az("az staticwebapp secrets list", locals())


def reset_api_key(name, no_wait=None, resource_group=None):
    '''
    Reset the deployment token for the static app.
    '''
    return _call_az("az staticwebapp secrets reset-api-key", locals())


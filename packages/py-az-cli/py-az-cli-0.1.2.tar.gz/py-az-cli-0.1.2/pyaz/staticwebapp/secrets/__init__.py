from ... pyaz_utils import call_az

def list(name, resource_group=None):
    '''
    List the deployment token for the static app.
    '''
    return call_az("az staticwebapp secrets list", locals())


def reset_api_key(name, no_wait=None, resource_group=None):
    '''
    Reset the deployment token for the static app.
    '''
    return call_az("az staticwebapp secrets reset-api-key", locals())


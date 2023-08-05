from ... pyaz_utils import call_az

def list(name, resource_group=None):
    '''
    list the private link resources supported for a registry
    '''
    return call_az("az acr private-link-resource list", locals())


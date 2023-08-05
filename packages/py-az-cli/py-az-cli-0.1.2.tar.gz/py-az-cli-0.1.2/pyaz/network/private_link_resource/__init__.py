from ... pyaz_utils import call_az

def list(id=None, name=None, resource_group=None, type=None):
    '''
    List all private link resources.
    '''
    return call_az("az network private-link-resource list", locals())


from ... pyaz_utils import _call_az

def list(id=None, name=None, resource_group=None, type=None):
    '''
    List all private link resources.
    '''
    return _call_az("az network private-link-resource list", locals())


from ... pyaz_utils import _call_az

def delete(name, resource_group, yes=None):
    '''
    Delete a network profile.
    '''
    return _call_az("az network profile delete", locals())


def list(resource_group=None):
    '''
    List network profiles.
    '''
    return _call_az("az network profile list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a network profile.
    '''
    return _call_az("az network profile show", locals())


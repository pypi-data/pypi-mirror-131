from ... pyaz_utils import call_az

def delete(name, resource_group, yes=None):
    '''
    Delete a network profile.
    '''
    return call_az("az network profile delete", locals())


def list(resource_group=None):
    '''
    List network profiles.
    '''
    return call_az("az network profile list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a network profile.
    '''
    return call_az("az network profile show", locals())


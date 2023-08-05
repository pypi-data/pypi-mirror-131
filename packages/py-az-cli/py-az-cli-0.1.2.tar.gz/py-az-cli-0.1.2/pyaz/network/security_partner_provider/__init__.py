from ... pyaz_utils import call_az

def create(name, provider, resource_group, vhub, location=None, tags=None):
    '''
    Create a Azure security partner provider.
    '''
    return call_az("az network security-partner-provider create", locals())


def update(name, resource_group, add=None, force_string=None, provider=None, remove=None, set=None, tags=None, vhub=None):
    '''
    Update a Azure security partner provider.
    '''
    return call_az("az network security-partner-provider update", locals())


def show(name, resource_group):
    '''
    Show a Azure security partner provider.
    '''
    return call_az("az network security-partner-provider show", locals())


def list(resource_group=None):
    '''
    List all Azure security partner provider.
    '''
    return call_az("az network security-partner-provider list", locals())


def delete(name, resource_group):
    '''
    Delete a Azure security partner provider.
    '''
    return call_az("az network security-partner-provider delete", locals())


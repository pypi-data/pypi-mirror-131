from ... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Show CDN profile details.
    '''
    return call_az("az cdn profile show", locals())


def usage(name, resource_group):
    return call_az("az cdn profile usage", locals())


def delete(name, resource_group):
    '''
    Delete a CDN profile.
    '''
    return call_az("az cdn profile delete", locals())


def list(resource_group=None):
    '''
    List CDN profiles.
    '''
    return call_az("az cdn profile list", locals())


def create(name, resource_group, location=None, sku=None, tags=None):
    '''
    Create a new CDN profile.
    '''
    return call_az("az cdn profile create", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update a CDN profile.
    '''
    return call_az("az cdn profile update", locals())


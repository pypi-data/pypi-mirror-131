from ... pyaz_utils import call_az

def show(profile_name, resource_group):
    '''
    Show details of an AFD profile.
    '''
    return call_az("az afd profile show", locals())


def delete(profile_name, resource_group):
    '''
    Delete an AFD profile.
    '''
    return call_az("az afd profile delete", locals())


def update(profile_name, resource_group, tags):
    '''
    Update an AFD profile.
    '''
    return call_az("az afd profile update", locals())


def list(resource_group=None):
    '''
    List AFD profiles.
    '''
    return call_az("az afd profile list", locals())


def create(profile_name, resource_group, sku, tags=None):
    '''
    Create a new AFD profile.
    '''
    return call_az("az afd profile create", locals())


def usage(profile_name, resource_group):
    '''
    List resource usage within the specific AFD profile.
    '''
    return call_az("az afd profile usage", locals())


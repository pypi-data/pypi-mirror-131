from ... pyaz_utils import call_az

def show(endpoint_name, profile_name, resource_group):
    '''
    Show details of an endpoint within the specified profile.
    '''
    return call_az("az afd endpoint show", locals())


def list(profile_name, resource_group):
    '''
    List all the endpoints within the specified profile.
    '''
    return call_az("az afd endpoint list", locals())


def purge(content_paths, endpoint_name, profile_name, resource_group, domains=None, no_wait=None):
    '''
    Removes cached contents from Azure Front Door.
    '''
    return call_az("az afd endpoint purge", locals())


def delete(endpoint_name, profile_name, resource_group, yes=None):
    '''
    Delete an endpoint within the specified profile.
    '''
    return call_az("az afd endpoint delete", locals())


def update(endpoint_name, profile_name, resource_group, enabled_state=None, origin_response_timeout_seconds=None, tags=None):
    '''
    Update an endpoint within the specified profile.
    '''
    return call_az("az afd endpoint update", locals())


def create(enabled_state, endpoint_name, origin_response_timeout_seconds, profile_name, resource_group, tags=None):
    '''
    Creates an endpoint within the specified profile.
    '''
    return call_az("az afd endpoint create", locals())


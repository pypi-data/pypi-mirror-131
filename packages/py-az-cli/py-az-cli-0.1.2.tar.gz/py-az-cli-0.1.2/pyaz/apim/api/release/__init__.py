from .... pyaz_utils import call_az

def list(api_id, resource_group, service_name):
    '''
    Lists all releases of an API.
    '''
    return call_az("az apim api release list", locals())


def show(api_id, release_id, resource_group, service_name):
    '''
    Returns the details of an API release.
    '''
    return call_az("az apim api release show", locals())


def create(api_id, api_revision, resource_group, service_name, if_match=None, notes=None, release_id=None):
    '''
    Creates a new Release for the API.
    '''
    return call_az("az apim api release create", locals())


def update(api_id, release_id, resource_group, service_name, add=None, api_id1=None, force_string=None, if_match=None, notes=None, remove=None, set=None):
    '''
    Updates the details of the release of the API specified by its identifier.
    '''
    return call_az("az apim api release update", locals())


def delete(api_id, release_id, resource_group, service_name, if_match=None):
    '''
    Deletes the specified release in the API.
    '''
    return call_az("az apim api release delete", locals())


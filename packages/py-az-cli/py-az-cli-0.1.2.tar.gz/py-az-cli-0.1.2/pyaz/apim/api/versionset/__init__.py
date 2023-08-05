from .... pyaz_utils import call_az

def list(resource_group, service_name):
    '''
    Lists a collection of API Version Sets in the specified service instance.
    '''
    return call_az("az apim api versionset list", locals())


def show(resource_group, service_name, version_set_id):
    '''
    Gets the details of the Api Version Set specified by its identifier.
    '''
    return call_az("az apim api versionset show", locals())


def create(display_name, resource_group, service_name, versioning_scheme, description=None, if_match=None, version_header_name=None, version_query_name=None, version_set_id=None):
    '''
    Creates a Api Version Set.
    '''
    return call_az("az apim api versionset create", locals())


def update(resource_group, service_name, version_set_id, add=None, description=None, display_name=None, force_string=None, if_match=None, remove=None, set=None, version_header_name=None, version_query_name=None, versioning_scheme=None):
    '''
    Updates the details of the Api VersionSet specified by its identifier.
    '''
    return call_az("az apim api versionset update", locals())


def delete(resource_group, service_name, version_set_id, if_match=None):
    '''
    Deletes specific Api Version Set.
    '''
    return call_az("az apim api versionset delete", locals())


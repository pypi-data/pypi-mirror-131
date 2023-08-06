from .... pyaz_utils import _call_az

def list(api_id, resource_group, service_name):
    '''
    Lists all revisions of an API.
    '''
    return _call_az("az apim api revision list", locals())


def create(api_id, api_revision, resource_group, service_name, api_revision_description=None):
    '''
    Create API revision.
    '''
    return _call_az("az apim api revision create", locals())


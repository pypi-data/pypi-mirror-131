from .... pyaz_utils import call_az

def list(api_id, resource_group, service_name):
    '''
    List a collection of the operations for the specified API.
    '''
    return call_az("az apim api operation list", locals())


def show(api_id, operation_id, resource_group, service_name):
    '''
    Gets the details of the API Operation specified by its identifier.
    '''
    return call_az("az apim api operation show", locals())


def create(api_id, display_name, method, resource_group, service_name, url_template, description=None, if_match=None, operation_id=None, template_parameters=None):
    '''
    Creates a new operation in the API
    '''
    return call_az("az apim api operation create", locals())


def update(api_id, operation_id, resource_group, service_name, add=None, description=None, display_name=None, force_string=None, if_match=None, method=None, remove=None, set=None, url_template=None):
    '''
    Updates the details of the operation in the API specified by its identifier.
    '''
    return call_az("az apim api operation update", locals())


def delete(api_id, operation_id, resource_group, service_name, if_match=None):
    '''
    Deletes the specified operation in the API.
    '''
    return call_az("az apim api operation delete", locals())


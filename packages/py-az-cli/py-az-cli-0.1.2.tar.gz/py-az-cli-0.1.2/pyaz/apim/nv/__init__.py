from ... pyaz_utils import call_az

def create(display_name, named_value_id, resource_group, service_name, secret=None, tags=None, value=None):
    '''
    Create an API Management Named Value.
    '''
    return call_az("az apim nv create", locals())


def show(named_value_id, resource_group, service_name):
    '''
    Show details of an API Management Named Value.
    '''
    return call_az("az apim nv show", locals())


def list(resource_group, service_name):
    '''
    List API Management Named Values.
    '''
    return call_az("az apim nv list", locals())


def delete(named_value_id, resource_group, service_name, yes=None):
    '''
    Delete an API Management Named Value.
    '''
    return call_az("az apim nv delete", locals())


def show_secret(named_value_id, resource_group, service_name):
    '''
    Gets the secret of an API Management Named Value.
    '''
    return call_az("az apim nv show-secret", locals())


def update(named_value_id, resource_group, service_name, add=None, force_string=None, if_match=None, remove=None, secret=None, set=None, tags=None, value=None):
    '''
    Update an API Management Named Value.
    '''
    return call_az("az apim nv update", locals())


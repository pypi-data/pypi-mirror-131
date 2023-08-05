from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List redirect configurations.
    '''
    return call_az("az network application-gateway redirect-config list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a redirect configuration.
    '''
    return call_az("az network application-gateway redirect-config show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a redirect configuration.
    '''
    return call_az("az network application-gateway redirect-config delete", locals())


def create(gateway_name, name, resource_group, type, include_path=None, include_query_string=None, no_wait=None, target_listener=None, target_url=None):
    '''
    Create a redirect configuration.
    '''
    return call_az("az network application-gateway redirect-config create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, include_path=None, include_query_string=None, no_wait=None, remove=None, set=None, target_listener=None, target_url=None, type=None):
    '''
    Update a redirect configuration.
    '''
    return call_az("az network application-gateway redirect-config update", locals())


from ... pyaz_utils import call_az

def show(endpoint_name, name, profile_name, resource_group):
    return call_az("az cdn origin show", locals())


def list(endpoint_name, profile_name, resource_group):
    return call_az("az cdn origin list", locals())


def create(endpoint_name, host_name, name, profile_name, resource_group, disabled=None, http_port=None, https_port=None, origin_host_header=None, priority=None, private_link_approval_message=None, private_link_location=None, private_link_resource_id=None, weight=None):
    '''
    Create an origin.
    '''
    return call_az("az cdn origin create", locals())


def update(endpoint_name, name, profile_name, resource_group, disabled=None, host_name=None, http_port=None, https_port=None, origin_host_header=None, priority=None, private_link_approval_message=None, private_link_location=None, private_link_resource_id=None, weight=None):
    '''
    Update an origin.
    '''
    return call_az("az cdn origin update", locals())


def delete(endpoint_name, name, profile_name, resource_group, yes=None):
    return call_az("az cdn origin delete", locals())


from ... pyaz_utils import call_az

def show(origin_group_name, origin_name, profile_name, resource_group):
    return call_az("az afd origin show", locals())


def list(origin_group_name, profile_name, resource_group):
    return call_az("az afd origin list", locals())


def create(enabled_state, host_name, origin_group_name, origin_name, profile_name, resource_group, enable_private_link=None, http_port=None, https_port=None, origin_host_header=None, priority=None, private_link_location=None, private_link_request_message=None, private_link_resource=None, private_link_sub_resource_type=None, weight=None):
    '''
    Create an AFD origin.
    '''
    return call_az("az afd origin create", locals())


def update(origin_group_name, origin_name, profile_name, resource_group, enable_private_link=None, enabled_state=None, host_name=None, http_port=None, https_port=None, origin_host_header=None, priority=None, private_link_location=None, private_link_request_message=None, private_link_resource=None, private_link_sub_resource_type=None, weight=None):
    '''
    Update the settings of the specified AFD origin.
    '''
    return call_az("az afd origin update", locals())


def delete(origin_group_name, origin_name, profile_name, resource_group, yes=None):
    return call_az("az afd origin delete", locals())


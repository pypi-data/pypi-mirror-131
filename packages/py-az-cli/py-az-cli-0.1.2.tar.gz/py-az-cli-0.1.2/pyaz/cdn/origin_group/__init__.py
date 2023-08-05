from ... pyaz_utils import call_az

def show(endpoint_name, name, profile_name, resource_group):
    return call_az("az cdn origin-group show", locals())


def list(endpoint_name, profile_name, resource_group):
    return call_az("az cdn origin-group list", locals())


def create(endpoint_name, name, profile_name, resource_group, origins=None, probe_interval=None, probe_method=None, probe_path=None, probe_protocol=None):
    '''
    Create an origin group.
    '''
    return call_az("az cdn origin-group create", locals())


def update(endpoint_name, name, profile_name, resource_group, origins=None, probe_interval=None, probe_method=None, probe_path=None, probe_protocol=None):
    '''
    Update an origin group.
    '''
    return call_az("az cdn origin-group update", locals())


def delete(endpoint_name, name, profile_name, resource_group, yes=None):
    return call_az("az cdn origin-group delete", locals())


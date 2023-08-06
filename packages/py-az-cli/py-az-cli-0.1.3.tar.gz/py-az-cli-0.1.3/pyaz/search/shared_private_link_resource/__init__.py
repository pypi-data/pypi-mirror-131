from ... pyaz_utils import _call_az

def list(resource_group, service_name):
    return _call_az("az search shared-private-link-resource list", locals())


def show(name, resource_group, service_name):
    return _call_az("az search shared-private-link-resource show", locals())


def delete(name, resource_group, service_name, yes=None):
    return _call_az("az search shared-private-link-resource delete", locals())


def create(group_id, name, resource_group, resource_id, service_name, no_wait=None, request_message=None):
    return _call_az("az search shared-private-link-resource create", locals())


def update(group_id, name, request_message, resource_group, resource_id, service_name, no_wait=None):
    return _call_az("az search shared-private-link-resource update", locals())


def wait(name, resource_group, service_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for async shared private link resource operations.
    '''
    return _call_az("az search shared-private-link-resource wait", locals())


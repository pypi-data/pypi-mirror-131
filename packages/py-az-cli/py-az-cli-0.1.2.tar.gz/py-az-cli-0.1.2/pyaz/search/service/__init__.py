from ... pyaz_utils import call_az

def list(resource_group):
    return call_az("az search service list", locals())


def show(name, resource_group):
    return call_az("az search service show", locals())


def delete(name, resource_group, yes=None):
    return call_az("az search service delete", locals())


def update(name, resource_group, add=None, force_string=None, identity_type=None, ip_rules=None, no_wait=None, partition_count=None, public_network_access=None, remove=None, replica_count=None, set=None):
    '''
    Update partition and replica of the given search service.
    '''
    return call_az("az search service update", locals())


def create(name, resource_group, sku, identity_type=None, ip_rules=None, location=None, no_wait=None, partition_count=None, public_network_access=None, replica_count=None):
    '''
    Creates a Search service in the given resource group.
    '''
    return call_az("az search service create", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for async service operations.
    '''
    return call_az("az search service wait", locals())


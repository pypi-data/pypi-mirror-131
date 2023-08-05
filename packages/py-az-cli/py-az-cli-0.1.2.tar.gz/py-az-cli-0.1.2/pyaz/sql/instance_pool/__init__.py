from ... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Get the details for an instance pool.
    '''
    return call_az("az sql instance-pool show", locals())


def list(resource_group=None):
    '''
    List available instance pools.
    '''
    return call_az("az sql instance-pool list", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update an instance pool.
    '''
    return call_az("az sql instance-pool update", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete an instance pool.
    '''
    return call_az("az sql instance-pool delete", locals())


def create(capacity, family, location, name, resource_group, subnet, tier, license_type=None, no_wait=None, tags=None, vnet_name=None):
    '''
    Create an instance pool.
    '''
    return call_az("az sql instance-pool create", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for an instance pool to reach a desired state.
    '''
    return call_az("az sql instance-pool wait", locals())


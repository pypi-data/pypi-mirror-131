from .... pyaz_utils import call_az

def create(name, resource_group, sku_capacity, identity_type=None, location=None, no_wait=None, sku_name=None, tags=None):
    '''
    Create a cluster instance.
    '''
    return call_az("az monitor log-analytics cluster create", locals())


def update(name, resource_group, key_name=None, key_vault_uri=None, key_version=None, sku_capacity=None, tags=None):
    '''
    Update a cluster instance.
    '''
    return call_az("az monitor log-analytics cluster update", locals())


def show(name, resource_group):
    '''
    Show the properties of a cluster instance.
    '''
    return call_az("az monitor log-analytics cluster show", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a cluster instance.
    '''
    return call_az("az monitor log-analytics cluster delete", locals())


def list(resource_group=None):
    '''
    Gets all cluster instances in a resource group or in current subscription.
    '''
    return call_az("az monitor log-analytics cluster list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the cluster is met.
    '''
    return call_az("az monitor log-analytics cluster wait", locals())


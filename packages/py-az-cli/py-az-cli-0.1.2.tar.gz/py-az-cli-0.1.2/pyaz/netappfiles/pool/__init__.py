from ... pyaz_utils import call_az

def show(account_name, pool_name, resource_group):
    '''
    Get the specified ANF pool.
    '''
    return call_az("az netappfiles pool show", locals())


def list(account_name, resource_group):
    '''
    L:ist the ANF pools for the specified account.
    '''
    return call_az("az netappfiles pool list", locals())


def delete(account_name, pool_name, resource_group):
    '''
    Delete the specified ANF pool.
    '''
    return call_az("az netappfiles pool delete", locals())


def create(account_name, location, pool_name, resource_group, service_level, size, cool_access=None, encryption_type=None, qos_type=None, tags=None):
    '''
    Create a new Azure NetApp Files (ANF) pool.
    '''
    return call_az("az netappfiles pool create", locals())


def update(account_name, pool_name, resource_group, add=None, force_string=None, qos_type=None, remove=None, set=None, size=None, tags=None):
    '''
    Update the tags of the specified ANF pool.
    '''
    return call_az("az netappfiles pool update", locals())


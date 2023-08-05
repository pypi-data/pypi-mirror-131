from ... pyaz_utils import call_az

def show(name, resource_group, server):
    return call_az("az sql failover-group show", locals())


def list(resource_group, server):
    return call_az("az sql failover-group list", locals())


def create(name, partner_server, resource_group, server, add_db=None, failover_policy=None, grace_period=None, partner_resource_group=None):
    '''
    Creates a failover group.
    '''
    return call_az("az sql failover-group create", locals())


def update(name, resource_group, server, add=None, add_db=None, failover_policy=None, force_string=None, grace_period=None, remove=None, remove_db=None, set=None):
    '''
    Updates the failover group.
    '''
    return call_az("az sql failover-group update", locals())


def delete(name, resource_group, server):
    return call_az("az sql failover-group delete", locals())


def set_primary(name, resource_group, server, allow_data_loss=None):
    '''
    Set the primary of the failover group by failing over all databases from the current primary server.
    '''
    return call_az("az sql failover-group set-primary", locals())


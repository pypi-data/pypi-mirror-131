from ... pyaz_utils import call_az

def show(location, name, resource_group):
    return call_az("az sql instance-failover-group show", locals())


def create(name, partner_mi, partner_resource_group, resource_group, source_mi, failover_policy=None, grace_period=None):
    '''
    Creates an instance failover group between two connected managed instances.
    '''
    return call_az("az sql instance-failover-group create", locals())


def update(location, name, resource_group, add=None, failover_policy=None, force_string=None, grace_period=None, remove=None, set=None):
    '''
    Updates the instance failover group.
    '''
    return call_az("az sql instance-failover-group update", locals())


def delete(location, name, resource_group):
    return call_az("az sql instance-failover-group delete", locals())


def set_primary(location, name, resource_group, allow_data_loss=None):
    '''
    Set the primary of the instance failover group by failing over all databases from the current primary managed instance.
    '''
    return call_az("az sql instance-failover-group set-primary", locals())


from ..... pyaz_utils import call_az

def show(account_name, policy_id, rule_id, resource_group=None):
    '''
    Show the properties of specified rule in Object Replication Service Policy.
    '''
    return call_az("az storage account or-policy rule show", locals())


def list(account_name, policy_id, resource_group=None):
    '''
    List all the rules in the specified Object Replication Service Policy.
    '''
    return call_az("az storage account or-policy rule list", locals())


def add(account_name, destination_container, policy_id, source_container, min_creation_time=None, prefix_match=None, resource_group=None):
    '''
    Add rule to the specified Object Replication Service Policy.
    '''
    return call_az("az storage account or-policy rule add", locals())


def update(account_name, policy_id, rule_id, destination_container=None, min_creation_time=None, prefix_match=None, resource_group=None, source_container=None):
    '''
    Update rule properties to Object Replication Service Policy.
    '''
    return call_az("az storage account or-policy rule update", locals())


def remove(account_name, policy_id, rule_id, resource_group=None):
    '''
    Remove the specified rule from the specified Object Replication Service Policy.
    '''
    return call_az("az storage account or-policy rule remove", locals())


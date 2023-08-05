from .... pyaz_utils import call_az
from . import rule


def show(account_name, policy_id, resource_group=None):
    '''
    Show the properties of specified Object Replication Service Policy for storage account.
    '''
    return call_az("az storage account or-policy show", locals())


def list(account_name, resource_group=None):
    '''
    List Object Replication Service Policies associated with the specified storage account.
    '''
    return call_az("az storage account or-policy list", locals())


def create(account_name, destination_account=None, destination_container=None, min_creation_time=None, policy=None, policy_id=None, prefix_match=None, resource_group=None, rule_id=None, source_account=None, source_container=None):
    '''
    Create Object Replication Service Policy for storage account.
    '''
    return call_az("az storage account or-policy create", locals())


def update(account_name, add=None, destination_account=None, force_string=None, policy=None, policy_id=None, remove=None, resource_group=None, set=None, source_account=None):
    '''
    Update Object Replication Service Policy properties for storage account.
    '''
    return call_az("az storage account or-policy update", locals())


def delete(account_name, policy_id, resource_group=None):
    '''
    Delete specified Object Replication Service Policy associated with the specified storage account.
    '''
    return call_az("az storage account or-policy delete", locals())


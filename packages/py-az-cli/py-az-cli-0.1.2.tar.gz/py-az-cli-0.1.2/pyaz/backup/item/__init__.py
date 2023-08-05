from ... pyaz_utils import call_az

def show(container_name, name, resource_group, vault_name, backup_management_type=None, use_secondary_region=None, workload_type=None):
    '''
    Show details of a particular backed up item.
    '''
    return call_az("az backup item show", locals())


def list(resource_group, vault_name, backup_management_type=None, container_name=None, use_secondary_region=None, workload_type=None):
    '''
    List all backed up items within a container.
    '''
    return call_az("az backup item list", locals())


def set_policy(container_name, name, policy_name, resource_group, vault_name, backup_management_type=None, workload_type=None):
    '''
    Update the policy associated with this item. Use this to change policies of the backup item.
    '''
    return call_az("az backup item set-policy", locals())


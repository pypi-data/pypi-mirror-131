from ... pyaz_utils import call_az

def get_default_for_vm(resource_group, vault_name):
    '''
    Get the default policy with default values to backup a VM.
    '''
    return call_az("az backup policy get-default-for-vm", locals())


def show(name, resource_group, vault_name):
    '''
    Show details of a particular policy.
    '''
    return call_az("az backup policy show", locals())


def list(resource_group, vault_name, backup_management_type=None, workload_type=None):
    '''
    List all policies for a Recovery services vault.
    '''
    return call_az("az backup policy list", locals())


def list_associated_items(name, resource_group, vault_name, backup_management_type=None):
    '''
    List all items protected by a backup policy.
    '''
    return call_az("az backup policy list-associated-items", locals())


def set(resource_group, vault_name, backup_management_type=None, fix_for_inconsistent_items=None, name=None, policy=None):
    '''
    Update the existing policy with the provided details.
    '''
    return call_az("az backup policy set", locals())


def delete(name, resource_group, vault_name):
    '''
    Delete a backup policy which doesn't have any associated backup items.
    '''
    return call_az("az backup policy delete", locals())


def create(backup_management_type, name, policy, resource_group, vault_name, workload_type=None):
    '''
    Create a new policy for the given BackupManagementType and workloadType.
    '''
    return call_az("az backup policy create", locals())


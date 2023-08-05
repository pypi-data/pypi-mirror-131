from ... pyaz_utils import call_az

def check_vm(resource_group=None, vm=None, vm_id=None):
    '''
    Find out whether the virtual machine is protected or not. If protected, it returns the recovery services vault ID, otherwise it returns empty.
    '''
    return call_az("az backup protection check-vm", locals())


def enable_for_vm(policy_name, resource_group, vault_name, vm, disk_list_setting=None, diskslist=None, exclude_all_data_disks=None):
    '''
    Start protecting a previously unprotected Azure VM as per the specified policy to a Recovery services vault.
    '''
    return call_az("az backup protection enable-for-vm", locals())


def update_for_vm(container_name, item_name, resource_group, vault_name, disk_list_setting=None, diskslist=None, exclude_all_data_disks=None):
    '''
    Update disk exclusion settings associated with a backed up VM item.
    '''
    return call_az("az backup protection update-for-vm", locals())


def backup_now(item_name, resource_group, vault_name, backup_management_type=None, backup_type=None, container_name=None, enable_compression=None, retain_until=None, workload_type=None):
    '''
    Perform an on-demand backup of a backed up item.
    '''
    return call_az("az backup protection backup-now", locals())


def disable(container_name, item_name, resource_group, vault_name, backup_management_type=None, delete_backup_data=None, workload_type=None, yes=None):
    '''
    Stop protecting a backed up item. Can retain the backed up data forever or choose to delete it.
    '''
    return call_az("az backup protection disable", locals())


def enable_for_azurefileshare(azure_file_share, policy_name, resource_group, storage_account, vault_name):
    '''
    Start protecting a previously unprotected Azure File share within an Azure Storage account as per the specified policy to a Recovery services vault.
    '''
    return call_az("az backup protection enable-for-azurefileshare", locals())


def enable_for_azurewl(policy_name, protectable_item_name, protectable_item_type, resource_group, server_name, vault_name, workload_type):
    '''
    Start protecting a previously unprotected workload within an Azure VM as per the specified policy to a Recovery services vault. Provide the workload details as a protectable item.
    '''
    return call_az("az backup protection enable-for-azurewl", locals())


def auto_enable_for_azurewl(policy_name, protectable_item_name, protectable_item_type, resource_group, server_name, vault_name, workload_type):
    '''
    Automatically protect all existing unprotected DBs and any DB which will be added later with the given policy.
    '''
    return call_az("az backup protection auto-enable-for-azurewl", locals())


def auto_disable_for_azurewl(protectable_item_name, protectable_item_type, resource_group, server_name, vault_name, workload_type):
    '''
    Disable auto-protection for the specified protectable item.
    '''
    return call_az("az backup protection auto-disable-for-azurewl", locals())


def resume(container_name, item_name, policy_name, resource_group, vault_name, backup_management_type=None, workload_type=None):
    '''
    Resume backup for the associated backup item. Use this to change the policy associated with the backup item.
    '''
    return call_az("az backup protection resume", locals())


def undelete(container_name, item_name, resource_group, vault_name, backup_management_type=None, workload_type=None):
    '''
    Rehydrate an item from softdeleted state to stop protection with retained data state.
    '''
    return call_az("az backup protection undelete", locals())


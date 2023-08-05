from ... pyaz_utils import call_az
from . import files


def restore_disks(container_name, item_name, resource_group, rp_name, storage_account, vault_name, disk_encryption_set_id=None, diskslist=None, mi_system_assigned=None, mi_user_assigned=None, rehydration_duration=None, rehydration_priority=None, restore_as_unmanaged_disks=None, restore_only_osdisk=None, restore_to_staging_storage_account=None, target_resource_group=None, target_zone=None, use_secondary_region=None):
    '''
    Restore disks of the backed VM from the specified recovery point.
    '''
    return call_az("az backup restore restore-disks", locals())


def restore_azurefileshare(container_name, item_name, resolve_conflict, resource_group, restore_mode, rp_name, vault_name, target_file_share=None, target_folder=None, target_storage_account=None):
    '''
    Restore backed up Azure file shares to the same file-share or another file-share in registered storage accounts.
    '''
    return call_az("az backup restore restore-azurefileshare", locals())


def restore_azurefiles(container_name, item_name, resolve_conflict, resource_group, restore_mode, rp_name, vault_name, source_file_path=None, source_file_type=None, target_file_share=None, target_folder=None, target_storage_account=None):
    '''
    Restore backed up Azure files within a file-share to the same file-share or another file-share in registered storage accounts.
    '''
    return call_az("az backup restore restore-azurefiles", locals())


def restore_azurewl(recovery_config, resource_group, vault_name, rehydration_duration=None, rehydration_priority=None, use_secondary_region=None):
    '''
    Restore backed up Azure Workloads in a Recovery services vault to another registered container or to the same container.
    '''
    return call_az("az backup restore restore-azurewl", locals())


from ... pyaz_utils import call_az

def show(container_name, item_name, resource_group, restore_mode, vault_name, backup_management_type=None, filepath=None, from_full_rp_name=None, log_point_in_time=None, rp_name=None, target_container_name=None, target_item_name=None, target_resource_group=None, target_server_name=None, target_server_type=None, target_vault_name=None, workload_type=None):
    '''
    Construct the recovery configuration of an Azure workload backed up item.
    '''
    return call_az("az backup recoveryconfig show", locals())


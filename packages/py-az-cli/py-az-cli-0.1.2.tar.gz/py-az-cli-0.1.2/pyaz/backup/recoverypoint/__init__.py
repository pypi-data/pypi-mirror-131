from ... pyaz_utils import call_az

def show(container_name, item_name, name, resource_group, vault_name, backup_management_type=None, use_secondary_region=None, workload_type=None):
    '''
    Shows details of a particular recovery point.
    '''
    return call_az("az backup recoverypoint show", locals())


def list(container_name, item_name, resource_group, vault_name, backup_management_type=None, end_date=None, is_ready_for_move=None, recommended_for_archive=None, start_date=None, target_tier=None, tier=None, use_secondary_region=None, workload_type=None):
    '''
    List all recovery points of a backed up item.
    '''
    return call_az("az backup recoverypoint list", locals())


def move(container_name, destination_tier, item_name, name, resource_group, source_tier, vault_name, backup_management_type=None, workload_type=None):
    '''
    Move a particular recovery point of a backed up item from one tier to another tier.
    '''
    return call_az("az backup recoverypoint move", locals())


def show_log_chain(container_name, item_name, resource_group, vault_name, backup_management_type=None, end_date=None, start_date=None, use_secondary_region=None, workload_type=None):
    '''
    List the start and end points of the unbroken log chain(s) of the given backup item.
    '''
    return call_az("az backup recoverypoint show-log-chain", locals())


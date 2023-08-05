from ... pyaz_utils import call_az
from . import backup, export_policy, replication


def show(account_name, pool_name, resource_group, volume_name):
    '''
    Get the specified ANF volume.
    '''
    return call_az("az netappfiles volume show", locals())


def list(account_name, pool_name, resource_group):
    '''
    List the ANF Pools for the specified account.
    '''
    return call_az("az netappfiles volume list", locals())


def delete(account_name, pool_name, resource_group, volume_name):
    '''
    Delete the specified ANF volume.
    '''
    return call_az("az netappfiles volume delete", locals())


def create(account_name, file_path, location, pool_name, resource_group, usage_threshold, vnet, volume_name, allowed_clients=None, avs_data_store=None, backup_enabled=None, backup_id=None, backup_policy_id=None, chown_mode=None, cifs=None, cool_access=None, coolness_period=None, default_group_quota=None, default_user_quota=None, encryption_key_source=None, endpoint_type=None, has_root_access=None, is_def_quota_enabled=None, kerberos5_r=None, kerberos5_rw=None, kerberos5i_r=None, kerberos5i_rw=None, kerberos5p_r=None, kerberos5p_rw=None, kerberos_enabled=None, ldap_enabled=None, network_features=None, policy_enforced=None, protocol_types=None, remote_volume_resource_id=None, replication_schedule=None, rule_index=None, security_style=None, service_level=None, smb_continuously_avl=None, smb_encryption=None, snapshot_dir_visible=None, snapshot_id=None, snapshot_policy_id=None, subnet=None, tags=None, throughput_mibps=None, unix_permissions=None, unix_read_only=None, unix_read_write=None, vault_id=None, volume_type=None):
    '''
    Create a new Azure NetApp Files (ANF) volume. Export policies are applied with the subgroup commands but note that volumes are always created with a default export policy
    '''
    return call_az("az netappfiles volume create", locals())


def update(account_name, pool_name, resource_group, volume_name, add=None, backup_enabled=None, backup_policy_id=None, default_group_quota=None, default_user_quota=None, force_string=None, is_def_quota_enabled=None, policy_enforced=None, remove=None, service_level=None, set=None, snapshot_policy_id=None, tags=None, throughput_mibps=None, usage_threshold=None, vault_id=None):
    '''
    Update the specified ANF volume with the values provided. Unspecified values will remain unchanged. Export policies are amended/created with the subgroup commands
    '''
    return call_az("az netappfiles volume update", locals())


def revert(account_name, pool_name, resource_group, snapshot_id, volume_name):
    '''
    Revert a volume to one of its snapshots.
    '''
    return call_az("az netappfiles volume revert", locals())


def pool_change(account_name, new_pool_resource_id, pool_name, resource_group, volume_name):
    '''
    Change pool for an Azure NetApp Files (ANF) volume.
    '''
    return call_az("az netappfiles volume pool-change", locals())


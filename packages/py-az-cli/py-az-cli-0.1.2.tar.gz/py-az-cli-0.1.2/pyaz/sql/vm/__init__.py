from ... pyaz_utils import call_az
from . import group


def update(name, resource_group, add=None, backup_pwd=None, backup_schedule_type=None, backup_system_dbs=None, connectivity_type=None, credential_name=None, day_of_week=None, enable_auto_backup=None, enable_auto_patching=None, enable_encryption=None, enable_key_vault_credential=None, enable_r_services=None, force_string=None, full_backup_duration=None, full_backup_frequency=None, full_backup_start_hour=None, image_sku=None, key_vault=None, license_type=None, log_backup_frequency=None, maintenance_window_duration=None, maintenance_window_start_hour=None, port=None, remove=None, retention_period=None, sa_key=None, set=None, sp_name=None, sp_secret=None, sql_mgmt_type=None, sql_workload_type=None, storage_account=None, tags=None, yes=None):
    '''
    Updates the properties of a SQL virtual machine.
    '''
    return call_az("az sql vm update", locals())


def show(name, resource_group, expand=None):
    return call_az("az sql vm show", locals())


def list(resource_group=None):
    return call_az("az sql vm list", locals())


def add_to_group(name, resource_group, sqlvm_group, operator_acc_pwd=None, service_acc_pwd=None):
    '''
    Adds SQL virtual machine to a SQL virtual machine group.
    '''
    return call_az("az sql vm add-to-group", locals())


def remove_from_group(name, resource_group):
    '''
    Remove SQL virtual machine from its current SQL virtual machine group.
    '''
    return call_az("az sql vm remove-from-group", locals())


def delete(name, resource_group, yes=None):
    return call_az("az sql vm delete", locals())


def create(name, resource_group, backup_pwd=None, backup_schedule_type=None, backup_system_dbs=None, connectivity_type=None, credential_name=None, day_of_week=None, enable_auto_backup=None, enable_auto_patching=None, enable_encryption=None, enable_key_vault_credential=None, enable_r_services=None, full_backup_duration=None, full_backup_frequency=None, full_backup_start_hour=None, image_offer=None, image_sku=None, key_vault=None, license_type=None, location=None, log_backup_frequency=None, maintenance_window_duration=None, maintenance_window_start_hour=None, port=None, retention_period=None, sa_key=None, sp_name=None, sp_secret=None, sql_auth_update_pwd=None, sql_auth_update_username=None, sql_mgmt_type=None, sql_workload_type=None, storage_account=None, tags=None):
    '''
    Creates a SQL virtual machine.
    '''
    return call_az("az sql vm create", locals())


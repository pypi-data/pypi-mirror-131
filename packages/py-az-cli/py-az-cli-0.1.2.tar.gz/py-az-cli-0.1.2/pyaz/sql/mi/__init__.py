from ... pyaz_utils import call_az
from . import ad_admin, ad_only_auth, key, op, tde_key


def create(name, resource_group, subnet, admin_password=None, admin_user=None, assign_identity=None, backup_storage_redundancy=None, capacity=None, collation=None, enable_ad_only_auth=None, external_admin_name=None, external_admin_principal_type=None, external_admin_sid=None, family=None, identity_type=None, key_id=None, license_type=None, location=None, maint_config_id=None, minimal_tls_version=None, no_wait=None, primary_user_assigned_identity_id=None, proxy_override=None, public_data_endpoint_enabled=None, storage=None, tags=None, tier=None, timezone_id=None, user_assigned_identity_id=None, vnet_name=None, yes=None):
    '''
    Create a managed instance.
    '''
    return call_az("az sql mi create", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a managed instance.
    '''
    return call_az("az sql mi delete", locals())


def show(name, resource_group, expand_ad_admin=None):
    '''
    Get the details for a managed instance.
    '''
    return call_az("az sql mi show", locals())


def list(expand_ad_admin=None, resource_group=None):
    '''
    List available managed instances.
    '''
    return call_az("az sql mi list", locals())


def update(name, resource_group, add=None, admin_password=None, assign_identity=None, capacity=None, family=None, force_string=None, identity_type=None, key_id=None, license_type=None, maint_config_id=None, minimal_tls_version=None, no_wait=None, primary_user_assigned_identity_id=None, proxy_override=None, public_data_endpoint_enabled=None, remove=None, set=None, storage=None, subnet=None, tags=None, tier=None, user_assigned_identity_id=None, vnet_name=None):
    '''
    Update a managed instance.
    '''
    return call_az("az sql mi update", locals())


def failover(name, resource_group, no_wait=None, replica_type=None):
    '''
    Failover a managed instance.
    '''
    return call_az("az sql mi failover", locals())


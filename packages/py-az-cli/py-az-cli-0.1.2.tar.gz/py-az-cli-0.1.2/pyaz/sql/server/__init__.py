from ... pyaz_utils import call_az
from . import ad_admin, ad_only_auth, audit_policy, conn_policy, dns_alias, firewall_rule, key, outbound_firewall_rule, tde_key, vnet_rule


def create(name, resource_group, admin_password=None, admin_user=None, assign_identity=None, enable_ad_only_auth=None, enable_public_network=None, external_admin_name=None, external_admin_principal_type=None, external_admin_sid=None, identity_type=None, key_id=None, location=None, minimal_tls_version=None, no_wait=None, primary_user_assigned_identity_id=None, restrict_outbound_network_access=None, user_assigned_identity_id=None):
    '''
    Create a server.
    '''
    return call_az("az sql server create", locals())


def delete(name, resource_group, yes=None):
    return call_az("az sql server delete", locals())


def show(name, resource_group, expand_ad_admin=None):
    return call_az("az sql server show", locals())


def list(expand_ad_admin=None, resource_group=None):
    '''
    List available servers.
    '''
    return call_az("az sql server list", locals())


def update(name, resource_group, add=None, admin_password=None, assign_identity=None, enable_public_network=None, force_string=None, identity_type=None, key_id=None, minimal_tls_version=None, no_wait=None, primary_user_assigned_identity_id=None, remove=None, restrict_outbound_network_access=None, set=None, user_assigned_identity_id=None):
    '''
    Update a server.
    '''
    return call_az("az sql server update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the SQL server is met.
    '''
    return call_az("az sql server wait", locals())


def list_usages(name, resource_group):
    return call_az("az sql server list-usages", locals())


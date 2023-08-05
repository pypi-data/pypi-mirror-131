from ... pyaz_utils import call_az
from . import ad_admin, configuration, firewall_rule, key, private_endpoint_connection, private_link_resource, replica, vnet_rule


def create(admin_password=None, admin_user=None, assign_identity=None, auto_grow=None, backup_retention=None, geo_redundant_backup=None, infrastructure_encryption=None, location=None, minimal_tls_version=None, name=None, public_network_access=None, resource_group=None, sku_name=None, ssl_enforcement=None, storage_size=None, tags=None, version=None):
    '''
    Create a server.
    '''
    return call_az("az mysql server create", locals())


def restore(name, resource_group, restore_point_in_time, source_server, no_wait=None):
    '''
    Restore a server from backup.
    '''
    return call_az("az mysql server restore", locals())


def georestore(location, name, resource_group, source_server, backup_retention=None, geo_redundant_backup=None, no_wait=None, sku_name=None):
    '''
    Geo-restore a server from backup.
    '''
    return call_az("az mysql server georestore", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a server.
    '''
    return call_az("az mysql server delete", locals())


def show(name, resource_group):
    '''
    Get the details of a server.
    '''
    return call_az("az mysql server show", locals())


def list(resource_group=None):
    '''
    List available servers.
    '''
    return call_az("az mysql server list", locals())


def update(name, resource_group, add=None, admin_password=None, assign_identity=None, auto_grow=None, backup_retention=None, force_string=None, minimal_tls_version=None, public_network_access=None, remove=None, set=None, sku_name=None, ssl_enforcement=None, storage_size=None, tags=None):
    '''
    Update a server.
    '''
    return call_az("az mysql server update", locals())


def wait(name, resource_group, custom=None, exists=None, interval=None, timeout=None):
    '''
    Wait for server to satisfy certain conditions.
    '''
    return call_az("az mysql server wait", locals())


def restart(name, resource_group):
    '''
    Restart a server.
    '''
    return call_az("az mysql server restart", locals())


def start(name, resource_group):
    '''
    Start a stopped server.
    '''
    return call_az("az mysql server start", locals())


def stop(name, resource_group):
    '''
    Stop a running server.
    '''
    return call_az("az mysql server stop", locals())


def upgrade(name, resource_group, target_server_version):
    '''
    Upgrade mysql server to a higher version, like 5.6 to 5.7.
    '''
    return call_az("az mysql server upgrade", locals())


def list_skus(location):
    '''
    List available sku's in the given region.
    '''
    return call_az("az mysql server list-skus", locals())


def show_connection_string(admin_password=None, admin_user=None, database_name=None, server_name=None):
    '''
    Show the connection strings for a MySQL server database.
    '''
    return call_az("az mysql server show-connection-string", locals())


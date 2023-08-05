from ... pyaz_utils import call_az
from . import configuration, firewall_rule, private_endpoint_connection, private_link_resource, replica, vnet_rule


def create(admin_password=None, admin_user=None, assign_identity=None, auto_grow=None, backup_retention=None, geo_redundant_backup=None, infrastructure_encryption=None, location=None, name=None, public_network_access=None, resource_group=None, sku_name=None, ssl_enforcement=None, storage_size=None, tags=None, version=None):
    '''
    Create a server.
    '''
    return call_az("az mariadb server create", locals())


def restore(name, resource_group, restore_point_in_time, source_server, no_wait=None):
    '''
    Restore a server from backup.
    '''
    return call_az("az mariadb server restore", locals())


def georestore(location, name, resource_group, source_server, backup_retention=None, geo_redundant_backup=None, no_wait=None, sku_name=None):
    '''
    Geo-restore a server from backup.
    '''
    return call_az("az mariadb server georestore", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a server.
    '''
    return call_az("az mariadb server delete", locals())


def show(name, resource_group):
    '''
    Get the details of a server.
    '''
    return call_az("az mariadb server show", locals())


def list(resource_group=None):
    '''
    List available servers.
    '''
    return call_az("az mariadb server list", locals())


def update(name, resource_group, add=None, admin_password=None, assign_identity=None, auto_grow=None, backup_retention=None, force_string=None, public_network_access=None, remove=None, set=None, sku_name=None, ssl_enforcement=None, storage_size=None, tags=None):
    '''
    Update a server.
    '''
    return call_az("az mariadb server update", locals())


def wait(name, resource_group, custom=None, exists=None, interval=None, timeout=None):
    '''
    Wait for server to satisfy certain conditions.
    '''
    return call_az("az mariadb server wait", locals())


def restart(name, resource_group):
    '''
    Restart a server.
    '''
    return call_az("az mariadb server restart", locals())


def start(name, resource_group):
    '''
    Start a stopped server.
    '''
    return call_az("az mariadb server start", locals())


def stop(name, resource_group):
    '''
    Stop a running server.
    '''
    return call_az("az mariadb server stop", locals())


def list_skus(location):
    '''
    List available sku's in the given region.
    '''
    return call_az("az mariadb server list-skus", locals())


def show_connection_string(admin_password=None, admin_user=None, database_name=None, server_name=None):
    '''
    Show the connection strings for a MariaDB server database.
    '''
    return call_az("az mariadb server show-connection-string", locals())


from ... pyaz_utils import call_az
from . import db, deploy, firewall_rule, migration, parameter


def create(address_prefixes=None, admin_password=None, admin_user=None, backup_retention=None, database_name=None, high_availability=None, location=None, name=None, private_dns_zone=None, public_access=None, resource_group=None, sku_name=None, standby_zone=None, storage_size=None, subnet=None, subnet_prefixes=None, tags=None, tier=None, version=None, vnet=None, yes=None, zone=None):
    '''
    Create a PostgreSQL flexible server.
    '''
    return call_az("az postgres flexible-server create", locals())


def restore(name, resource_group, source_server, address_prefixes=None, no_wait=None, private_dns_zone=None, restore_time=None, subnet=None, subnet_prefixes=None, vnet=None, yes=None, zone=None):
    '''
    Restore a flexible server from backup.
    '''
    return call_az("az postgres flexible-server restore", locals())


def start(name, resource_group):
    '''
    Start a flexible server.
    '''
    return call_az("az postgres flexible-server start", locals())


def stop(name=None, resource_group=None):
    '''
    Stop a flexible server.
    '''
    return call_az("az postgres flexible-server stop", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a flexible server.
    '''
    return call_az("az postgres flexible-server delete", locals())


def show(name, resource_group):
    '''
    Get the details of a flexible server.
    '''
    return call_az("az postgres flexible-server show", locals())


def list(resource_group=None):
    '''
    List available flexible servers.
    '''
    return call_az("az postgres flexible-server list", locals())


def update(name, resource_group, add=None, admin_password=None, backup_retention=None, force_string=None, high_availability=None, maintenance_window=None, remove=None, set=None, sku_name=None, standby_zone=None, storage_size=None, tags=None, tier=None):
    '''
    Update a flexible server.
    '''
    return call_az("az postgres flexible-server update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for the flexible server to satisfy certain conditions.
    '''
    return call_az("az postgres flexible-server wait", locals())


def restart(name, resource_group, failover=None):
    '''
    Restart a flexible server.
    '''
    return call_az("az postgres flexible-server restart", locals())


def list_skus(location):
    '''
    Lists available sku's in the given region.
    '''
    return call_az("az postgres flexible-server list-skus", locals())


def show_connection_string(admin_password=None, admin_user=None, database_name=None, server_name=None):
    '''
    Show the connection strings for a PostgreSQL flexible-server database.
    '''
    return call_az("az postgres flexible-server show-connection-string", locals())


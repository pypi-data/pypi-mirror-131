from .. pyaz_utils import call_az
from . import firewall_rules, patch_schedule, server_link


def create(location, name, resource_group, sku, vm_size, enable_non_ssl_port=None, minimum_tls_version=None, redis_configuration=None, redis_version=None, replicas_per_master=None, shard_count=None, static_ip=None, subnet_id=None, tags=None, tenant_settings=None, zones=None):
    '''
    Create new Redis Cache instance.
    '''
    return call_az("az redis create", locals())


def delete(name, resource_group, yes=None):
    return call_az("az redis delete", locals())


def export(container, name, prefix, resource_group, file_format=None):
    '''
    Export data stored in a Redis cache.
    '''
    return call_az("az redis export", locals())


def force_reboot(name, reboot_type, resource_group, shard_id=None):
    '''
    Reboot specified Redis node(s).
    '''
    return call_az("az redis force-reboot", locals())


def import_method(files, name, resource_group, file_format=None):
    '''
    Import data into Redis cache.
    '''
    return call_az("az redis import-method", locals())


def import_(files, name, resource_group, file_format=None):
    '''
    Import data into a Redis cache.
    '''
    return call_az("az redis import", locals())


def list(resource_group=None):
    '''
    List Redis Caches.
    '''
    return call_az("az redis list", locals())


def list_keys(name, resource_group):
    return call_az("az redis list-keys", locals())


def regenerate_keys(key_type, name, resource_group):
    '''
    Regenerate Redis cache's access keys.
    '''
    return call_az("az redis regenerate-keys", locals())


def show(name, resource_group):
    return call_az("az redis show", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, sku=None, vm_size=None):
    '''
    Update a Redis cache.
    '''
    return call_az("az redis update", locals())


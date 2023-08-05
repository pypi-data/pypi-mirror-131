from ... pyaz_utils import call_az
from . import access_restriction, appsettings, backup, connection_string, container, hostname, snapshot, ssl, storage_account


def set(name, resource_group, always_on=None, auto_heal_enabled=None, ftps_state=None, generic_configurations=None, http20_enabled=None, java_container=None, java_container_version=None, java_version=None, linux_fx_version=None, min_tls_version=None, net_framework_version=None, number_of_workers=None, php_version=None, prewarmed_instance_count=None, python_version=None, remote_debugging_enabled=None, slot=None, startup_file=None, use_32bit_worker_process=None, vnet_route_all_enabled=None, web_sockets_enabled=None, windows_fx_version=None):
    '''
    Set a web app's configuration.
    '''
    return call_az("az webapp config set", locals())


def show(name, resource_group, slot=None):
    '''
    Get the details of a web app's configuration.
    '''
    return call_az("az webapp config show", locals())


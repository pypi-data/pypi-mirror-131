from .. pyaz_utils import call_az
from . import dcos, kubernetes


def browse(name, resource_group, disable_browser=None, ssh_key_file=None):
    '''
    Show the dashboard for a service container's orchestrator in a web browser.
    '''
    return call_az("az acs browse", locals())


def create(name, resource_group, admin_password=None, admin_username=None, agent_count=None, agent_osdisk_size=None, agent_ports=None, agent_profiles=None, agent_storage_profile=None, agent_vm_size=None, agent_vnet_subnet_id=None, api_version=None, client_secret=None, deployment_name=None, dns_prefix=None, generate_ssh_keys=None, location=None, master_count=None, master_first_consecutive_static_ip=None, master_osdisk_size=None, master_profile=None, master_storage_profile=None, master_vm_size=None, master_vnet_subnet_id=None, no_wait=None, orchestrator_type=None, orchestrator_version=None, service_principal=None, ssh_key_value=None, tags=None, validate=None, windows=None):
    '''
    Create a new container service.
    '''
    return call_az("az acs create", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a container service.
    '''
    return call_az("az acs delete", locals())


def list(resource_group=None):
    '''
    List container services.
    '''
    return call_az("az acs list", locals())


def list_locations():
    '''
    List locations where Azure Container Service is in preview and in production.
    '''
    return call_az("az acs list-locations", locals())


def scale(name, new_agent_count, resource_group):
    '''
    Change the private agent count of a container service.
    '''
    return call_az("az acs scale", locals())


def show(name, resource_group):
    '''
    Show the details for a container service.
    '''
    return call_az("az acs show", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for a container service to reach a desired state.
    '''
    return call_az("az acs wait", locals())


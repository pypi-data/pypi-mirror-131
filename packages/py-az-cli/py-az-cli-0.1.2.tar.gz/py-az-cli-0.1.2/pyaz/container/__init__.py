from .. pyaz_utils import call_az

def list(resource_group=None):
    '''
    List container groups.
    '''
    return call_az("az container list", locals())


def create(resource_group, acr_identity=None, assign_identity=None, azure_file_volume_account_key=None, azure_file_volume_account_name=None, azure_file_volume_mount_path=None, azure_file_volume_share_name=None, command_line=None, cpu=None, dns_name_label=None, environment_variables=None, file=None, gitrepo_dir=None, gitrepo_mount_path=None, gitrepo_revision=None, gitrepo_url=None, image=None, ip_address=None, location=None, log_analytics_workspace=None, log_analytics_workspace_key=None, memory=None, name=None, no_wait=None, os_type=None, ports=None, protocol=None, registry_login_server=None, registry_password=None, registry_username=None, restart_policy=None, role=None, scope=None, secrets=None, secrets_mount_path=None, secure_environment_variables=None, subnet=None, subnet_address_prefix=None, vnet=None, vnet_address_prefix=None, vnet_name=None, zone=None):
    '''
    Create a container group.
    '''
    return call_az("az container create", locals())


def show(name, resource_group):
    '''
    Get the details of a container group.
    '''
    return call_az("az container show", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a container group.
    '''
    return call_az("az container delete", locals())


def logs(name, resource_group, container_name=None, follow=None):
    '''
    Examine the logs for a container in a container group.
    '''
    return call_az("az container logs", locals())


def exec(exec_command, name, resource_group, container_name=None):
    '''
    Execute a command from within a running container of a container group.
    '''
    return call_az("az container exec", locals())


def export(file, name, resource_group):
    '''
    Export a container group in yaml format.
    '''
    return call_az("az container export", locals())


def attach(name, resource_group, container_name=None):
    '''
    Attach local standard output and error streams to a container in a container group.
    '''
    return call_az("az container attach", locals())


def restart(name, resource_group, no_wait=None):
    return call_az("az container restart", locals())


def stop(name, resource_group):
    return call_az("az container stop", locals())


def start(name, resource_group, no_wait=None):
    return call_az("az container start", locals())


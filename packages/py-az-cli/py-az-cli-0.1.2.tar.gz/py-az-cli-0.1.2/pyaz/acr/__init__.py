from .. pyaz_utils import call_az
from . import agentpool, connected_registry, credential, encryption, helm, identity, network_rule, pack, private_endpoint_connection, private_link_resource, replication, repository, scope_map, task, taskrun, token, webhook


def check_name(name):
    '''
    Checks if an Azure Container Registry name is valid and available for use.
    '''
    return call_az("az acr check-name", locals())


def list(resource_group=None):
    '''
    Lists all the container registries under the current subscription.
    '''
    return call_az("az acr list", locals())


def create(name, resource_group, sku, admin_enabled=None, allow_exports=None, allow_trusted_services=None, default_action=None, identity=None, key_encryption_key=None, location=None, public_network_enabled=None, tags=None, workspace=None, zone_redundancy=None):
    '''
    Create an Azure Container Registry.
    '''
    return call_az("az acr create", locals())


def delete(name, resource_group=None, yes=None):
    '''
    Deletes an Azure Container Registry.
    '''
    return call_az("az acr delete", locals())


def show(name, resource_group=None):
    '''
    Get the details of an Azure Container Registry.
    '''
    return call_az("az acr show", locals())


def show_usage(name, resource_group=None):
    '''
    Get the storage usage for an Azure Container Registry.
    '''
    return call_az("az acr show-usage", locals())


def show_endpoints(name, resource_group=None):
    '''
    Display registry endpoints
    '''
    return call_az("az acr show-endpoints", locals())


def update(name, add=None, admin_enabled=None, allow_exports=None, allow_trusted_services=None, anonymous_pull_enabled=None, data_endpoint_enabled=None, default_action=None, force_string=None, public_network_enabled=None, remove=None, resource_group=None, set=None, sku=None, tags=None):
    '''
    Update an Azure Container Registry.
    '''
    return call_az("az acr update", locals())


def login(name, expose_token=None, password=None, resource_group=None, suffix=None, username=None):
    '''
    Log in to an Azure Container Registry through the Docker CLI.
    '''
    return call_az("az acr login", locals())


def import_(name, source, force=None, image=None, no_wait=None, password=None, registry=None, repository=None, resource_group=None, username=None):
    '''
    Imports an image to an Azure Container Registry from another Container Registry. Import removes the need to docker pull, docker tag, docker push. For larger images consider using `--no-wait`.
    '''
    return call_az("az acr import", locals())


def build(registry, agent_pool=None, auth_mode=None, build_arg=None, file=None, image=None, log_template=None, no_format=None, no_logs=None, no_push=None, no_wait=None, platform=None, resource_group=None, secret_build_arg=None, target=None, timeout=None):
    '''
    Queues a quick build, providing streaming logs for an Azure Container Registry.
    '''
    return call_az("az acr build", locals())


def run(registry, agent_pool=None, auth_mode=None, file=None, log_template=None, no_format=None, no_logs=None, no_wait=None, platform=None, resource_group=None, set=None, set_secret=None, timeout=None, values=None):
    '''
    Queues a quick run providing streamed logs for an Azure Container Registry.
    '''
    return call_az("az acr run", locals())


def check_health(ignore_errors=None, name=None, vnet=None, yes=None):
    '''
    Gets health information on the environment and optionally a target registry.
    '''
    return call_az("az acr check-health", locals())


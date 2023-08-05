from ... pyaz_utils import call_az
from . import credential, identity, timer


def create(name, registry, agent_pool=None, arg=None, assign_identity=None, auth_mode=None, base_image_trigger_enabled=None, base_image_trigger_name=None, base_image_trigger_type=None, commit_trigger_enabled=None, context=None, cpu=None, file=None, git_access_token=None, image=None, is_system_task=None, log_template=None, no_cache=None, no_push=None, platform=None, pull_request_trigger_enabled=None, resource_group=None, schedule=None, secret_arg=None, set=None, set_secret=None, source_trigger_name=None, status=None, target=None, timeout=None, update_trigger_endpoint=None, update_trigger_payload_type=None, values=None):
    '''
    Create a series of steps for building, testing and OS & Framework patching containers. Tasks support triggers from git commits and base image updates.
    '''
    return call_az("az acr task create", locals())


def show(name, registry, resource_group=None, with_secure_properties=None):
    '''
    Get the properties of a named task for an Azure Container Registry.
    '''
    return call_az("az acr task show", locals())


def list(registry, resource_group=None):
    '''
    List the tasks for an Azure Container Registry.
    '''
    return call_az("az acr task list", locals())


def delete(name, registry, resource_group=None, yes=None):
    '''
    Delete a task from an Azure Container Registry.
    '''
    return call_az("az acr task delete", locals())


def update(name, registry, agent_pool=None, arg=None, auth_mode=None, base_image_trigger_enabled=None, base_image_trigger_type=None, commit_trigger_enabled=None, context=None, cpu=None, file=None, git_access_token=None, image=None, log_template=None, no_cache=None, no_push=None, platform=None, pull_request_trigger_enabled=None, resource_group=None, secret_arg=None, set=None, set_secret=None, status=None, target=None, timeout=None, update_trigger_endpoint=None, update_trigger_payload_type=None, values=None):
    '''
    Update a task for an Azure Container Registry.
    '''
    return call_az("az acr task update", locals())


def run(name, registry, agent_pool=None, arg=None, context=None, file=None, log_template=None, no_logs=None, no_wait=None, resource_group=None, secret_arg=None, set=None, set_secret=None, target=None, update_trigger_token=None):
    '''
    Manually trigger a task that might otherwise be waiting for git commits or base image update triggers.
    '''
    return call_az("az acr task run", locals())


def list_runs(registry, image=None, name=None, resource_group=None, run_status=None, top=None):
    '''
    List all of the executed runs for an Azure Container Registry, with the ability to filter by a specific Task.
    '''
    return call_az("az acr task list-runs", locals())


def show_run(registry, run_id, resource_group=None):
    '''
    Get the properties of a specified run of an Azure Container Registry Task.
    '''
    return call_az("az acr task show-run", locals())


def cancel_run(registry, run_id, resource_group=None):
    '''
    Cancel a specified run of an Azure Container Registry.
    '''
    return call_az("az acr task cancel-run", locals())


def update_run(registry, run_id, no_archive=None, resource_group=None):
    '''
    Patch the run properties of an Azure Container Registry Task.
    '''
    return call_az("az acr task update-run", locals())


def logs(registry, image=None, name=None, resource_group=None, run_id=None):
    '''
    Show logs for a particular run. If no run-id is supplied, show logs for the last created run.
    '''
    return call_az("az acr task logs", locals())


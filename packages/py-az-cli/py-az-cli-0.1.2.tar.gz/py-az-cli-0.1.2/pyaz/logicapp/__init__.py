from .. pyaz_utils import call_az

def delete(name, resource_group, slot=None, yes=None):
    '''
    Delete a logic app.
    '''
    return call_az("az logicapp delete", locals())


def stop(name, resource_group, slot=None):
    '''
    Stop a logic app.
    '''
    return call_az("az logicapp stop", locals())


def start(name, resource_group, slot=None):
    '''
    Start a logic app.
    '''
    return call_az("az logicapp start", locals())


def restart(name, resource_group, slot=None):
    '''
    Restart a logic app.
    '''
    return call_az("az logicapp restart", locals())


def create(name, resource_group, storage_account, app_insights=None, app_insights_key=None, consumption_plan_location=None, deployment_container_image_name=None, deployment_local_git=None, deployment_source_branch=None, deployment_source_url=None, disable_app_insights=None, docker_registry_server_password=None, docker_registry_server_user=None, os_type=None, plan=None, tags=None):
    '''
    Create a logic app.
    '''
    return call_az("az logicapp create", locals())


def list(resource_group=None):
    '''
    List logic apps.
    '''
    return call_az("az logicapp list", locals())


def show(name, resource_group, slot=None):
    '''
    Get the details of a logic app.
    '''
    return call_az("az logicapp show", locals())


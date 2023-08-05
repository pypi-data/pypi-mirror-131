from ... pyaz_utils import call_az

def list(resource_group, filter=None):
    '''
    List deployments at resource group.
    '''
    return call_az("az deployment group list", locals())


def show(name, resource_group):
    '''
    Show a deployment at resource group.
    '''
    return call_az("az deployment group show", locals())


def delete(name, resource_group, no_wait=None):
    '''
    Delete a deployment at resource group.
    '''
    return call_az("az deployment group delete", locals())


def validate(resource_group, handle_extended_json_format=None, mode=None, name=None, no_prompt=None, parameters=None, query_string=None, rollback_on_error=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Validate whether a template is valid at resource group.
    '''
    return call_az("az deployment group validate", locals())


def create(resource_group, aux_subs=None, aux_tenants=None, confirm_with_what_if=None, handle_extended_json_format=None, mode=None, name=None, no_prompt=None, no_wait=None, parameters=None, proceed_if_no_change=None, query_string=None, rollback_on_error=None, template_file=None, template_spec=None, template_uri=None, what_if=None, what_if_exclude_change_types=None, what_if_result_format=None):
    '''
    Start a deployment at resource group.
    '''
    return call_az("az deployment group create", locals())


def what_if(resource_group, aux_tenants=None, exclude_change_types=None, mode=None, name=None, no_pretty_print=None, no_prompt=None, parameters=None, query_string=None, result_format=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Execute a deployment What-If operation at resource group scope.
    '''
    return call_az("az deployment group what-if", locals())


def export(name, resource_group):
    '''
    Export the template used for a deployment.
    '''
    return call_az("az deployment group export", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a deployment condition is met.
    '''
    return call_az("az deployment group wait", locals())


def cancel(name, resource_group):
    '''
    Cancel a deployment at resource group.
    '''
    return call_az("az deployment group cancel", locals())


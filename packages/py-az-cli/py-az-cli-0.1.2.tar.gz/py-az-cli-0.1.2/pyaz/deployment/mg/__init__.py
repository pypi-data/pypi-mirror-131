from ... pyaz_utils import call_az

def list(management_group_id, filter=None):
    '''
    List deployments at management group.
    '''
    return call_az("az deployment mg list", locals())


def show(management_group_id, name):
    '''
    Show a deployment at management group.
    '''
    return call_az("az deployment mg show", locals())


def delete(management_group_id, name, no_wait=None):
    '''
    Delete a deployment at management group.
    '''
    return call_az("az deployment mg delete", locals())


def validate(location, management_group_id, handle_extended_json_format=None, name=None, no_prompt=None, parameters=None, query_string=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Validate whether a template is valid at management group.
    '''
    return call_az("az deployment mg validate", locals())


def create(location, management_group_id, confirm_with_what_if=None, handle_extended_json_format=None, name=None, no_prompt=None, no_wait=None, parameters=None, proceed_if_no_change=None, query_string=None, template_file=None, template_spec=None, template_uri=None, what_if=None, what_if_exclude_change_types=None, what_if_result_format=None):
    '''
    Start a deployment at management group.
    '''
    return call_az("az deployment mg create", locals())


def what_if(location, management_group_id, exclude_change_types=None, name=None, no_pretty_print=None, no_prompt=None, parameters=None, query_string=None, result_format=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Execute a deployment What-If operation at management group scope.
    '''
    return call_az("az deployment mg what-if", locals())


def export(management_group_id, name):
    '''
    Export the template used for a deployment.
    '''
    return call_az("az deployment mg export", locals())


def wait(management_group_id, name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a deployment condition is met.
    '''
    return call_az("az deployment mg wait", locals())


def cancel(management_group_id, name):
    '''
    Cancel a deployment at management group.
    '''
    return call_az("az deployment mg cancel", locals())


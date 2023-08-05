from ... pyaz_utils import call_az

def list(filter=None):
    '''
    List deployments at subscription scope.
    '''
    return call_az("az deployment sub list", locals())


def show(name):
    '''
    Show a deployment at subscription scope.
    '''
    return call_az("az deployment sub show", locals())


def delete(name, no_wait=None):
    '''
    Delete a deployment at subscription scope.
    '''
    return call_az("az deployment sub delete", locals())


def validate(location, handle_extended_json_format=None, name=None, no_prompt=None, parameters=None, query_string=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Validate whether a template is valid at subscription scope.
    '''
    return call_az("az deployment sub validate", locals())


def create(location, confirm_with_what_if=None, handle_extended_json_format=None, name=None, no_prompt=None, no_wait=None, parameters=None, proceed_if_no_change=None, query_string=None, template_file=None, template_spec=None, template_uri=None, what_if=None, what_if_exclude_change_types=None, what_if_result_format=None):
    '''
    Start a deployment at subscription scope.
    '''
    return call_az("az deployment sub create", locals())


def what_if(location, exclude_change_types=None, name=None, no_pretty_print=None, no_prompt=None, parameters=None, query_string=None, result_format=None, template_file=None, template_spec=None, template_uri=None):
    '''
    Execute a deployment What-If operation at subscription scope.
    '''
    return call_az("az deployment sub what-if", locals())


def export(name):
    '''
    Export the template used for a deployment.
    '''
    return call_az("az deployment sub export", locals())


def wait(name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a deployment condition is met.
    '''
    return call_az("az deployment sub wait", locals())


def cancel(name):
    '''
    Cancel a deployment at subscription scope.
    '''
    return call_az("az deployment sub cancel", locals())


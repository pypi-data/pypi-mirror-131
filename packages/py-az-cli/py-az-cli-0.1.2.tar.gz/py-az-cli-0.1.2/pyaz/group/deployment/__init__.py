from ... pyaz_utils import call_az
from . import operation


def create(resource_group, aux_subs=None, aux_tenants=None, handle_extended_json_format=None, mode=None, name=None, no_prompt=None, no_wait=None, parameters=None, rollback_on_error=None, template_file=None, template_uri=None):
    '''
    Start a deployment.
    '''
    return call_az("az group deployment create", locals())


def list(resource_group, filter=None, top=None):
    return call_az("az group deployment list", locals())


def show(name, resource_group):
    return call_az("az group deployment show", locals())


def delete(name, resource_group, no_wait=None):
    return call_az("az group deployment delete", locals())


def validate(resource_group, handle_extended_json_format=None, mode=None, no_prompt=None, parameters=None, rollback_on_error=None, template_file=None, template_uri=None):
    '''
    Validate whether a template is syntactically correct.
    '''
    return call_az("az group deployment validate", locals())


def export(name, resource_group):
    '''
    Export the template used for a deployment.
    '''
    return call_az("az group deployment export", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a deployment condition is met.
    '''
    return call_az("az group deployment wait", locals())


def cancel(name, resource_group):
    return call_az("az group deployment cancel", locals())


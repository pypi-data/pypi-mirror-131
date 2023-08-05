from ... pyaz_utils import call_az
from . import categories, subscription


def create(name, resource, event_hub=None, event_hub_rule=None, export_to_resource_specific=None, logs=None, metrics=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, storage_account=None, workspace=None):
    '''
    Create diagnostic settings for the specified resource.
    '''
    return call_az("az monitor diagnostic-settings create", locals())


def show(name, resource, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    return call_az("az monitor diagnostic-settings show", locals())


def list(resource, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    return call_az("az monitor diagnostic-settings list", locals())


def delete(name, resource, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    return call_az("az monitor diagnostic-settings delete", locals())


def update(name, resource, add=None, force_string=None, remove=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, set=None):
    '''
    Update diagnostic settings.
    '''
    return call_az("az monitor diagnostic-settings update", locals())


from .. pyaz_utils import call_az
from . import definition


def create(kind, managed_rg_id, name, resource_group, location=None, managedapp_definition_id=None, parameters=None, plan_name=None, plan_product=None, plan_publisher=None, plan_version=None, tags=None):
    '''
    Create a managed application.
    '''
    return call_az("az managedapp create", locals())


def delete(name, resource_group):
    '''
    Delete a managed application.
    '''
    return call_az("az managedapp delete", locals())


def show(name=None, resource_group=None):
    return call_az("az managedapp show", locals())


def list(resource_group=None):
    '''
    List managed applications.
    '''
    return call_az("az managedapp list", locals())


from .. pyaz_utils import call_az
from . import project


def check_name(location, name):
    '''
    Check if a given DMS instance name is available in a given region as well as the name's validity.
    '''
    return call_az("az dms check-name", locals())


def check_status(name, resource_group):
    '''
    Perform a health check and return the status of the service and virtual machine size.
    '''
    return call_az("az dms check-status", locals())


def create(location, name, resource_group, sku_name, subnet, no_wait=None, tags=None):
    '''
    Create an instance of the Data Migration Service.
    '''
    return call_az("az dms create", locals())


def delete(name, resource_group, delete_running_tasks=None, no_wait=None, yes=None):
    '''
    Delete an instance of the Data Migration Service.
    '''
    return call_az("az dms delete", locals())


def list(resource_group=None):
    '''
    List the DMS instances within your currently configured subscription (to set this use "az account set"). If provided, only show the instances within a given resource group.
    '''
    return call_az("az dms list", locals())


def show(name, resource_group):
    '''
    Show the details for an instance of the Data Migration Service.
    '''
    return call_az("az dms show", locals())


def start(name, resource_group, no_wait=None):
    '''
    Start an instance of the Data Migration Service. It can then be used to run data migrations.
    '''
    return call_az("az dms start", locals())


def stop(name, resource_group, no_wait=None):
    '''
    Stop an instance of the Data Migration Service. While stopped, it can't be used to run data migrations and the owner won't be billed.
    '''
    return call_az("az dms stop", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the DMS instance is met.
    '''
    return call_az("az dms wait", locals())


def list_skus():
    '''
    List the SKUs that are supported by the Data Migration Service.
    '''
    return call_az("az dms list-skus", locals())


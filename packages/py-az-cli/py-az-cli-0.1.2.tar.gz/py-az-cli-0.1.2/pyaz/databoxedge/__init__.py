from .. pyaz_utils import call_az
from . import alert, bandwidth_schedule, device, order


def show_job(device_name, name, resource_group):
    '''
    Get the details of a specified job on a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge show-job", locals())


def list_node(device_name, resource_group):
    '''
    Get all the nodes currently configured under this Data Box Edge device.
    '''
    return call_az("az databoxedge list-node", locals())


def list_sku(filter=None):
    '''
    List all the available Skus in the region and information related to them.
    '''
    return call_az("az databoxedge list-sku", locals())


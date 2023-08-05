from .... pyaz_utils import call_az
from . import event_grid, event_hub, iot_hub


def list(database_name, kusto_pool_name, resource_group, workspace_name):
    '''
    Returns the list of data connections of the given Kusto pool database.
    '''
    return call_az("az synapse kusto data-connection list", locals())


def show(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name):
    '''
    Returns a data connection.
    '''
    return call_az("az synapse kusto data-connection show", locals())


def delete(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Deletes the data connection with the given name.
    '''
    return call_az("az synapse kusto data-connection delete", locals())


def wait(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the synapse kusto data-connection is met.
    '''
    return call_az("az synapse kusto data-connection wait", locals())


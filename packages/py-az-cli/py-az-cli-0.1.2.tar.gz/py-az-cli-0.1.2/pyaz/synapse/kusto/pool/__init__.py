from .... pyaz_utils import call_az

def list_sku(name, resource_group, workspace_name):
    '''
    Returns the SKUs available for the provided resource.
    '''
    return call_az("az synapse kusto pool list-sku", locals())


def list(resource_group, workspace_name):
    '''
    List all Kusto pools.
    '''
    return call_az("az synapse kusto pool list", locals())


def show(name, resource_group, workspace_name):
    '''
    Gets a Kusto pool.
    '''
    return call_az("az synapse kusto pool show", locals())


def delete(name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Deletes a Kusto pool.
    '''
    return call_az("az synapse kusto pool delete", locals())


def list_follower_database(name, resource_group, workspace_name):
    '''
    Returns a list of databases that are owned by this Kusto Pool and were followed by another Kusto Pool.
    '''
    return call_az("az synapse kusto pool list-follower-database", locals())


def list_language_extension(name, resource_group, workspace_name):
    '''
    Returns a list of language extensions that can run within KQL queries.
    '''
    return call_az("az synapse kusto pool list-language-extension", locals())


def start(name, resource_group, workspace_name, no_wait=None):
    '''
    Starts a Kusto pool.
    '''
    return call_az("az synapse kusto pool start", locals())


def stop(name, resource_group, workspace_name, no_wait=None):
    '''
    Stops a Kusto pool.
    '''
    return call_az("az synapse kusto pool stop", locals())


def wait(name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the synapse kusto pool is met.
    '''
    return call_az("az synapse kusto pool wait", locals())


def create(name, resource_group, sku, workspace_name, enable_purge=None, enable_streaming_ingest=None, if_match=None, if_none_match=None, location=None, no_wait=None, optimized_autoscale=None, tags=None, workspace_uid=None):
    '''
    Create a Kusto pool.
    '''
    return call_az("az synapse kusto pool create", locals())


def update(name, resource_group, workspace_name, enable_purge=None, enable_streaming_ingest=None, if_match=None, no_wait=None, optimized_autoscale=None, sku=None, tags=None, workspace_uid=None):
    '''
    Update a Kusto Kusto Pool.
    '''
    return call_az("az synapse kusto pool update", locals())


def add_language_extension(name, resource_group, workspace_name, no_wait=None, value=None):
    '''
    Add a list of language extensions that can run within KQL queries.
    '''
    return call_az("az synapse kusto pool add-language-extension", locals())


def detach_follower_database(attached_database_configuration_name, kusto_pool_resource_id, name, resource_group, workspace_name, no_wait=None):
    '''
    Detaches all followers of a database owned by this Kusto Pool.
    '''
    return call_az("az synapse kusto pool detach-follower-database", locals())


def remove_language_extension(name, resource_group, workspace_name, no_wait=None, value=None):
    '''
    Remove a list of language extensions that can run within KQL queries.
    '''
    return call_az("az synapse kusto pool remove-language-extension", locals())


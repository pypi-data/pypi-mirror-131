from .... pyaz_utils import call_az

def show(name, resource_group, workspace_name):
    '''
    Get a Spark pool.
    '''
    return call_az("az synapse spark pool show", locals())


def list(resource_group, workspace_name):
    '''
    List all Spark pools.
    '''
    return call_az("az synapse spark pool list", locals())


def create(name, node_count, node_size, resource_group, spark_version, workspace_name, delay=None, enable_auto_pause=None, enable_auto_scale=None, max_node_count=None, min_node_count=None, no_wait=None, node_size_family=None, spark_config_file_path=None, spark_events_folder=None, spark_log_folder=None, tags=None):
    '''
    Create a Spark pool.
    '''
    return call_az("az synapse spark pool create", locals())


def update(name, resource_group, workspace_name, delay=None, enable_auto_pause=None, enable_auto_scale=None, force=None, library_requirements=None, max_node_count=None, min_node_count=None, no_wait=None, node_count=None, node_size=None, package=None, package_action=None, spark_config_file_path=None, tags=None):
    '''
    Update the Spark pool.
    '''
    return call_az("az synapse spark pool update", locals())


def delete(name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Delete a Spark pool.
    '''
    return call_az("az synapse spark pool delete", locals())


def wait(big_data_pool_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a Spark pool is met.
    '''
    return call_az("az synapse spark pool wait", locals())


from .... pyaz_utils import call_az

def create(executor_size, executors, name, spark_pool_name, workspace_name, configuration=None, reference_files=None, tags=None):
    '''
    Create a Spark session.
    '''
    return call_az("az synapse spark session create", locals())


def list(spark_pool_name, workspace_name, from_index=None, size=None):
    '''
    List all Spark sessions.
    '''
    return call_az("az synapse spark session list", locals())


def show(livy_id, spark_pool_name, workspace_name):
    '''
    Get a Spark session.
    '''
    return call_az("az synapse spark session show", locals())


def cancel(livy_id, spark_pool_name, workspace_name, yes=None):
    '''
    Cancel a Spark session.
    '''
    return call_az("az synapse spark session cancel", locals())


def reset_timeout(livy_id, spark_pool_name, workspace_name):
    '''
    Reset a Spark session timeout time.
    '''
    return call_az("az synapse spark session reset-timeout", locals())


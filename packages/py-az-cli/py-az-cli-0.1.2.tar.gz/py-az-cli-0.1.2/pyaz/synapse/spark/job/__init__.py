from .... pyaz_utils import call_az

def submit(executor_size, executors, main_definition_file, name, spark_pool_name, workspace_name, archives=None, arguments=None, configuration=None, language=None, main_class_name=None, reference_files=None, tags=None):
    '''
    Submit a Spark job.
    '''
    return call_az("az synapse spark job submit", locals())


def list(spark_pool_name, workspace_name, from_index=None, size=None):
    '''
    List all Spark jobs.
    '''
    return call_az("az synapse spark job list", locals())


def show(livy_id, spark_pool_name, workspace_name):
    '''
    Get a Spark job.
    '''
    return call_az("az synapse spark job show", locals())


def cancel(livy_id, spark_pool_name, workspace_name, yes=None):
    '''
    Cancel a Spark job.
    '''
    return call_az("az synapse spark job cancel", locals())


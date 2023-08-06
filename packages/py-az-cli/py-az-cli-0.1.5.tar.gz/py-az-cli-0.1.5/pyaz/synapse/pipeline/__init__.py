from ... pyaz_utils import _call_az

def create(file, name, workspace_name, no_wait=None):
    '''
    Create a pipeline.
    '''
    return _call_az("az synapse pipeline create", locals())


def set(file, name, workspace_name, no_wait=None):
    '''
    Update an exist pipeline.
    '''
    return _call_az("az synapse pipeline set", locals())


def update(file, name, workspace_name, no_wait=None):
    '''
    Update an exist pipeline.
    '''
    return _call_az("az synapse pipeline update", locals())


def list(workspace_name):
    '''
    List pipelines.
    '''
    return _call_az("az synapse pipeline list", locals())


def show(name, workspace_name):
    '''
    Get a pipeline.
    '''
    return _call_az("az synapse pipeline show", locals())


def delete(name, workspace_name, no_wait=None, yes=None):
    '''
    Delete a pipeline.
    '''
    return _call_az("az synapse pipeline delete", locals())


def create_run(name, workspace_name, is_recovery=None, parameters=None, reference_pipeline_run_id=None, start_activity_name=None):
    '''
    Creates a run of a pipeline.
    '''
    return _call_az("az synapse pipeline create-run", locals())


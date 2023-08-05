from ... pyaz_utils import call_az

def query_by_workspace(last_updated_after, last_updated_before, workspace_name, continuation_token=None, filters=None, order_by=None):
    '''
    Query pipeline runs in the workspace based on input filter conditions.
    '''
    return call_az("az synapse pipeline-run query-by-workspace", locals())


def show(run_id, workspace_name):
    '''
    Get a pipeline run by its run ID.
    '''
    return call_az("az synapse pipeline-run show", locals())


def cancel(run_id, workspace_name, is_recursive=None, yes=None):
    '''
    Cancel a pipeline run by its run ID.
    '''
    return call_az("az synapse pipeline-run cancel", locals())


from ... pyaz_utils import call_az

def rerun(name, run_id, workspace_name):
    '''
    Rerun single trigger instance by runId.
    '''
    return call_az("az synapse trigger-run rerun", locals())


def cancel(name, run_id, workspace_name):
    '''
    Cancel a single trigger instance by runId.
    '''
    return call_az("az synapse trigger-run cancel", locals())


def query_by_workspace(last_updated_after, last_updated_before, workspace_name, continuation_token=None, filters=None, order_by=None):
    '''
    Query trigger runs in the workspace based on input filter conditions.
    '''
    return call_az("az synapse trigger-run query-by-workspace", locals())


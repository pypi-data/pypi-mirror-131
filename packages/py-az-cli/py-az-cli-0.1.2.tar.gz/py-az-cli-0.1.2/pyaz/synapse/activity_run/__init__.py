from ... pyaz_utils import call_az

def query_by_pipeline_run(last_updated_after, last_updated_before, name, run_id, workspace_name, continuation_token=None, filters=None, order_by=None):
    '''
    Query activity runs based on input filter conditions.
    '''
    return call_az("az synapse activity-run query-by-pipeline-run", locals())


from .... pyaz_utils import call_az

def list(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, select=None):
    return call_az("az batch task subtask list", locals())


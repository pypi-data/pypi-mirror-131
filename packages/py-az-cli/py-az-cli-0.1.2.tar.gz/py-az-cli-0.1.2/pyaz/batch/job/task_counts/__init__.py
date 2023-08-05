from .... pyaz_utils import call_az

def show(job_id, account_endpoint=None, account_key=None, account_name=None):
    return call_az("az batch job task-counts show", locals())


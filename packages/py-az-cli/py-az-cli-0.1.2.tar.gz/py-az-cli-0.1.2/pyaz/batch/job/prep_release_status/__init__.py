from .... pyaz_utils import call_az

def list(job_id, account_endpoint=None, account_key=None, account_name=None, filter=None, select=None):
    return call_az("az batch job prep-release-status list", locals())


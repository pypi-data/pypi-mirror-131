from .... pyaz_utils import _call_az

def list(job_id, account_endpoint=None, account_key=None, account_name=None, filter=None, select=None):
    return _call_az("az batch job prep-release-status list", locals())


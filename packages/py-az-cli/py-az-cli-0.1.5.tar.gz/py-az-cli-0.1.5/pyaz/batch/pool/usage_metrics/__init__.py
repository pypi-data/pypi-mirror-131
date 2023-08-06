from .... pyaz_utils import _call_az

def list(account_endpoint=None, account_key=None, account_name=None, end_time=None, filter=None, start_time=None):
    return _call_az("az batch pool usage-metrics list", locals())


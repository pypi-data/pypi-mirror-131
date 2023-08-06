from .... pyaz_utils import _call_az

def list(account_endpoint=None, account_key=None, account_name=None, filter=None):
    return _call_az("az batch pool node-counts list", locals())


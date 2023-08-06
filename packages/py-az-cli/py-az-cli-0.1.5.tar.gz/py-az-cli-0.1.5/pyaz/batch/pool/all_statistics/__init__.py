from .... pyaz_utils import _call_az

def show(account_endpoint=None, account_key=None, account_name=None):
    '''
    Get lifetime summary statistics for all of the pools in a Batch account.
    '''
    return _call_az("az batch pool all-statistics show", locals())


from .... pyaz_utils import call_az

def show(account_endpoint=None, account_key=None, account_name=None):
    '''
    Get lifetime summary statistics for all of the pools in a Batch account.
    '''
    return call_az("az batch pool all-statistics show", locals())


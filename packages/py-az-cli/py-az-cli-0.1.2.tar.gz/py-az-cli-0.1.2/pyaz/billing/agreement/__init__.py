from ... pyaz_utils import call_az

def list(account_name, expand=None):
    '''
    List the agreements for a billing account.
    '''
    return call_az("az billing agreement list", locals())


def show(account_name, name, expand=None):
    '''
    Get an agreement by ID.
    '''
    return call_az("az billing agreement show", locals())


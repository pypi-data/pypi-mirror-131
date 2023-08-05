from .... pyaz_utils import call_az

def list(account_endpoint=None, account_key=None, account_name=None):
    '''
    Lists all of the applications available in the specified account.
    '''
    return call_az("az batch application summary list", locals())


def show(application_id, account_endpoint=None, account_key=None, account_name=None):
    '''
    Gets information about the specified application.
    '''
    return call_az("az batch application summary show", locals())


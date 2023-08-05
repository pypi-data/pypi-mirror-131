from ... pyaz_utils import call_az

def create(certificate_file, thumbprint, account_endpoint=None, account_key=None, account_name=None, password=None):
    '''
    Add a certificate to a Batch account.
    '''
    return call_az("az batch certificate create", locals())


def delete(thumbprint, abort=None, account_endpoint=None, account_key=None, account_name=None, yes=None):
    '''
    Delete a certificate from a Batch account.
    '''
    return call_az("az batch certificate delete", locals())


def show(thumbprint, account_endpoint=None, account_key=None, account_name=None, select=None):
    return call_az("az batch certificate show", locals())


def list(account_endpoint=None, account_key=None, account_name=None, filter=None, select=None):
    return call_az("az batch certificate list", locals())


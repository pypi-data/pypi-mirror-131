from ... pyaz_utils import call_az

def list(account_name, filter=None, profile_name=None, search=None):
    '''
    List the customers that are billed to a billing account. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement.
    '''
    return call_az("az billing customer list", locals())


def show(account_name, name, expand=None):
    '''
    Get a customer by its ID. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement.
    '''
    return call_az("az billing customer show", locals())


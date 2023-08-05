from ... pyaz_utils import call_az

def list(expand=None):
    '''
    List the billing accounts that a user has access to.
    '''
    return call_az("az billing account list", locals())


def show(name, expand=None):
    '''
    Get a billing account by its ID.
    '''
    return call_az("az billing account show", locals())


def update(name, billing_profiles_value=None, departments=None, display_name=None, enrollment_accounts=None, no_wait=None, sold_to=None):
    '''
    Update the properties of a billing account. Currently, displayName and address can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing account update", locals())


def wait(name, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the billing account is met.
    '''
    return call_az("az billing account wait", locals())


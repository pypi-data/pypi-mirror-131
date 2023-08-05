from .... pyaz_utils import call_az

def list(account_name, profile_name):
    '''
    List the invoice sections that a user has access to. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing invoice section list", locals())


def show(account_name, name, profile_name):
    '''
    Get an invoice section by its ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing invoice section show", locals())


def create(account_name, name, profile_name, display_name=None, labels=None, no_wait=None):
    '''
    Creates or updates an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing invoice section create", locals())


def update(account_name, name, profile_name, display_name=None, labels=None, no_wait=None):
    '''
    Creates or updates an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing invoice section update", locals())


def wait(account_name, name, profile_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the billing invoice section is met.
    '''
    return call_az("az billing invoice section wait", locals())


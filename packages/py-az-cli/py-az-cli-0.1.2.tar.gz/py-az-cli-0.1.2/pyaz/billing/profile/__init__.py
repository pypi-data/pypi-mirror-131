from ... pyaz_utils import call_az

def list(account_name, expand=None):
    '''
    List the billing profiles that a user has access to. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing profile list", locals())


def show(account_name, name, expand=None):
    '''
    Get a billing profile by its ID. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing profile show", locals())


def create(account_name, name, bill_to=None, display_name=None, enabled_azure_plans=None, invoice_email_opt_in=None, invoice_sections_value=None, no_wait=None, po_number=None):
    '''
    Creates or updates a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing profile create", locals())


def update(account_name, name, bill_to=None, display_name=None, enabled_azure_plans=None, invoice_email_opt_in=None, invoice_sections_value=None, no_wait=None, po_number=None):
    '''
    Creates or updates a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing profile update", locals())


def wait(account_name, name, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the billing profile is met.
    '''
    return call_az("az billing profile wait", locals())


from ... pyaz_utils import call_az

def list(account_name, customer_name=None, invoice_section_name=None, profile_name=None):
    '''
    List the subscriptions for a billing account. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing subscription list", locals())


def show(account_name):
    '''
    Get a subscription by its ID. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement and Microsoft Partner Agreement.
    '''
    return call_az("az billing subscription show", locals())


def update(account_name, cost_center=None, sku_id=None, subscription_billing_status=None):
    '''
    Update the properties of a billing subscription. Currently, cost center can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing subscription update", locals())


def move(account_name, destination_invoice_section_id, no_wait=None):
    '''
    Moves a subscription's charges to a new invoice section. The new invoice section must belong to the same billing profile as the existing invoice section. This operation is supported for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing subscription move", locals())


def validate_move(account_name, destination_invoice_section_id):
    '''
    Validate if a subscription's charges can be moved to a new invoice section. This operation is supported for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing subscription validate-move", locals())


def wait(account_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the billing subscription is met.
    '''
    return call_az("az billing subscription wait", locals())


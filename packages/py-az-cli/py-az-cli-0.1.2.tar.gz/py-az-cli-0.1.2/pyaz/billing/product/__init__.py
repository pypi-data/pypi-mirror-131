from ... pyaz_utils import call_az

def list(account_name, customer_name=None, filter=None, invoice_section_name=None, profile_name=None):
    '''
    List the products for a billing account. These don't include products billed based on usage. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement.
    '''
    return call_az("az billing product list", locals())


def show(account_name, name):
    '''
    Get a product by ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing product show", locals())


def update(account_name, name, auto_renew=None, billing_frequency=None, status=None):
    '''
    Update the properties of a Product. Currently, auto renew can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing product update", locals())


def move(account_name, name, destination_invoice_section_id=None):
    '''
    Moves a product's charges to a new invoice section. The new invoice section must belong to the same billing profile as the existing invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing product move", locals())


def validate_move(account_name, name, destination_invoice_section_id=None):
    '''
    Validate if a product's charges can be moved to a new invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing product validate-move", locals())


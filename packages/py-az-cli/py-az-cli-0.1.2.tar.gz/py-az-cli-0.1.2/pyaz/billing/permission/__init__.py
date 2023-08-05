from ... pyaz_utils import call_az

def list(account_name, customer_name=None, invoice_section_name=None, profile_name=None):
    '''
    List the billing permissions the caller has on a billing account.
    '''
    return call_az("az billing permission list", locals())


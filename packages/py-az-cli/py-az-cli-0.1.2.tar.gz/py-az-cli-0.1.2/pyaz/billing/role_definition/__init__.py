from ... pyaz_utils import call_az

def list(account_name, invoice_section_name=None, profile_name=None):
    '''
    List the role definitions for a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement.
    '''
    return call_az("az billing role-definition list", locals())


def show(account_name, name, invoice_section_name=None, profile_name=None):
    '''
    Show the role definition details
    '''
    return call_az("az billing role-definition show", locals())


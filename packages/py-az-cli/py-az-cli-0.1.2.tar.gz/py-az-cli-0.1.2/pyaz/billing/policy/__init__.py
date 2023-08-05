from ... pyaz_utils import call_az

def update(account_name, customer_name=None, marketplace_purchases=None, profile_name=None, reservation_purchases=None, view_charges=None):
    '''
    Update the policies for a billing profile. This operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing policy update", locals())


def show(account_name, customer_name=None, profile_name=None):
    '''
    Show the policies for a customer or for a billing profile. This operation is supported only for billing accounts with agreement type Microsoft Partner Agreement."
    '''
    return call_az("az billing policy show", locals())


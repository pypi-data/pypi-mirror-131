from ... pyaz_utils import call_az
from . import section


def list(period_end_date, period_start_date, account_name=None, profile_name=None):
    '''
    List the invoices for a subscription.
    '''
    return call_az("az billing invoice list", locals())


def show(name, account_name=None, by_subscription=None):
    '''
    Get an invoice. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement.
    '''
    return call_az("az billing invoice show", locals())


def download(account_name=None, download_token=None, download_urls=None, invoice_name=None):
    '''
    Get URL to download invoice
    '''
    return call_az("az billing invoice download", locals())


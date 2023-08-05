from ... pyaz_utils import call_az

def list(account_name, invoice_name):
    '''
    List the transactions for an invoice. Transactions include purchases, refunds and Azure usage charges.
    '''
    return call_az("az billing transaction list", locals())


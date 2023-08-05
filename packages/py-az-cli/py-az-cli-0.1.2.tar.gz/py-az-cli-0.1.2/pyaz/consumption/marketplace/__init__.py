from ... pyaz_utils import call_az

def list(billing_period_name=None, end_date=None, start_date=None, top=None):
    '''
    List the marketplace for an Azure subscription within a billing period.
    '''
    return call_az("az consumption marketplace list", locals())


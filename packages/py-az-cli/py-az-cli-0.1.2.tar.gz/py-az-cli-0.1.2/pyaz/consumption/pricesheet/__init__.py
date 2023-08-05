from ... pyaz_utils import call_az

def show(billing_period_name=None, include_meter_details=None):
    '''
    Show the price sheet for an Azure subscription within a billing period.
    '''
    return call_az("az consumption pricesheet show", locals())


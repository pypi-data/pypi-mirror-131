from ... pyaz_utils import call_az

def list(billing_period_name=None, end_date=None, include_additional_properties=None, include_meter_details=None, start_date=None, top=None):
    '''
    List the details of Azure resource consumption, either as an invoice or within a billing period.
    '''
    return call_az("az consumption usage list", locals())


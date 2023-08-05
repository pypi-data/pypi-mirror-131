from ... pyaz_utils import call_az

def show():
    '''
    Get the billing properties for a subscription. This operation is not supported for billing accounts with agreement type Enterprise Agreement.
    '''
    return call_az("az billing property show", locals())


def update(cost_center=None):
    '''
    Update the billing property of a subscription. Currently, cost center can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement.
    '''
    return call_az("az billing property update", locals())


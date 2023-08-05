from ... pyaz_utils import call_az

def list(subscription_id):
    '''
    Get list of applicable reservation order ids.
    '''
    return call_az("az reservations reservation-order-id list", locals())


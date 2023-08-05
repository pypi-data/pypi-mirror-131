from ... pyaz_utils import call_az

def show(reserved_resource_type, subscription_id, location=None):
    '''
    Get catalog of available reservation.
    '''
    return call_az("az reservations catalog show", locals())


from ... pyaz_utils import _call_az

def show(reserved_resource_type, subscription_id, location=None):
    '''
    Get catalog of available reservation.
    '''
    return _call_az("az reservations catalog show", locals())


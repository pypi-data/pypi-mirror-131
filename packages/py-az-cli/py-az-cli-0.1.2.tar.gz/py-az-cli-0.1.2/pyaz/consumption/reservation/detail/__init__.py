from .... pyaz_utils import call_az

def list(end_date, reservation_order_id, start_date, reservation_id=None):
    '''
    List the details of a reservation by order id or reservation id.
    '''
    return call_az("az consumption reservation detail list", locals())


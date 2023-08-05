from .... pyaz_utils import call_az

def list(grain, reservation_order_id, end_date=None, reservation_id=None, start_date=None):
    '''
    List reservation summaries for daily or monthly by order Id or reservation id.
    '''
    return call_az("az consumption reservation summary list", locals())


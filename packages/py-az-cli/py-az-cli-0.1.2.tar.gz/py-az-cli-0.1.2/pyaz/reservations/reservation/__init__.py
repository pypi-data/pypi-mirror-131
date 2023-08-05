from ... pyaz_utils import call_az

def list(reservation_order_id):
    '''
    Get all reservations.
    '''
    return call_az("az reservations reservation list", locals())


def show(reservation_id, reservation_order_id, expand=None):
    '''
    Get details of a reservation.
    '''
    return call_az("az reservations reservation show", locals())


def list_history(reservation_id, reservation_order_id):
    '''
    Get history of a reservation.
    '''
    return call_az("az reservations reservation list-history", locals())


def update(applied_scope_type, reservation_id, reservation_order_id, applied_scopes=None, instance_flexibility=None):
    '''
    Updates the applied scopes of the reservation.
    '''
    return call_az("az reservations reservation update", locals())


def split(quantity_1, quantity_2, reservation_id, reservation_order_id):
    '''
    Split a reservation.
    '''
    return call_az("az reservations reservation split", locals())


def merge(reservation_id_1, reservation_id_2, reservation_order_id):
    '''
    Merge two reservations.
    '''
    return call_az("az reservations reservation merge", locals())


from ... pyaz_utils import call_az

def list():
    '''
    Get all reservation orders
    '''
    return call_az("az reservations reservation-order list", locals())


def show(reservation_order_id, expand=None):
    '''
    Get a specific reservation order.
    '''
    return call_az("az reservations reservation-order show", locals())


def calculate(applied_scope_type, billing_scope, display_name, quantity, reserved_resource_type, sku, term, applied_scope=None, billing_plan=None, instance_flexibility=None, location=None, renew=None):
    '''
    Calculate price for a reservation order.
    '''
    return call_az("az reservations reservation-order calculate", locals())


def purchase(applied_scope_type, billing_scope, display_name, quantity, reservation_order_id, reserved_resource_type, sku, term, applied_scope=None, billing_plan=None, instance_flexibility=None, location=None, renew=None):
    '''
    Purchase reservation order
    '''
    return call_az("az reservations reservation-order purchase", locals())


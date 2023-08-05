from .... pyaz_utils import call_az

def list(lb_name, resource_group):
    '''
    List inbound NAT address pools.
    '''
    return call_az("az network lb inbound-nat-pool list", locals())


def show(lb_name, name, resource_group):
    '''
    Get the details of an inbound NAT address pool.
    '''
    return call_az("az network lb inbound-nat-pool show", locals())


def delete(lb_name, name, resource_group):
    '''
    Delete an inbound NAT address pool.
    '''
    return call_az("az network lb inbound-nat-pool delete", locals())


def create(backend_port, frontend_port_range_end, frontend_port_range_start, lb_name, name, protocol, resource_group, enable_tcp_reset=None, floating_ip=None, frontend_ip_name=None, idle_timeout=None):
    '''
    Create an inbound NAT address pool.
    '''
    return call_az("az network lb inbound-nat-pool create", locals())


def update(lb_name, name, resource_group, add=None, backend_port=None, enable_tcp_reset=None, floating_ip=None, force_string=None, frontend_ip_name=None, frontend_port_range_end=None, frontend_port_range_start=None, idle_timeout=None, protocol=None, remove=None, set=None):
    '''
    Update an inbound NAT address pool.
    '''
    return call_az("az network lb inbound-nat-pool update", locals())


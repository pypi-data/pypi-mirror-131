from .... pyaz_utils import call_az

def list(lb_name, resource_group):
    '''
    List load balancing rules.
    '''
    return call_az("az network lb rule list", locals())


def show(lb_name, name, resource_group):
    '''
    Get the details of a load balancing rule.
    '''
    return call_az("az network lb rule show", locals())


def delete(lb_name, name, resource_group):
    '''
    Delete a load balancing rule.
    '''
    return call_az("az network lb rule delete", locals())


def create(backend_port, frontend_port, lb_name, name, protocol, resource_group, backend_pool_name=None, backend_pools_name=None, disable_outbound_snat=None, enable_tcp_reset=None, floating_ip=None, frontend_ip_name=None, idle_timeout=None, load_distribution=None, probe_name=None):
    '''
    Create a load balancing rule.
    '''
    return call_az("az network lb rule create", locals())


def update(lb_name, name, resource_group, add=None, backend_pool_name=None, backend_pools_name=None, backend_port=None, disable_outbound_snat=None, enable_tcp_reset=None, floating_ip=None, force_string=None, frontend_ip_name=None, frontend_port=None, idle_timeout=None, load_distribution=None, probe_name=None, protocol=None, remove=None, set=None):
    '''
    Update a load balancing rule.
    '''
    return call_az("az network lb rule update", locals())


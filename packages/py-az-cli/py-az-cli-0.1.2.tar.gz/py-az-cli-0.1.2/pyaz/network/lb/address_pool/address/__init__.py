from ..... pyaz_utils import call_az

def add(ip_address, lb_name, name, pool_name, resource_group, subnet=None, vnet=None):
    '''
    Add one backend address into the load balance backend address pool.
    '''
    return call_az("az network lb address-pool address add", locals())


def remove(lb_name, name, pool_name, resource_group):
    '''
    Remove one backend address from the load balance backend address pool.
    '''
    return call_az("az network lb address-pool address remove", locals())


def list(lb_name, pool_name, resource_group):
    '''
    List all backend addresses of the load balance backend address pool.
    '''
    return call_az("az network lb address-pool address list", locals())


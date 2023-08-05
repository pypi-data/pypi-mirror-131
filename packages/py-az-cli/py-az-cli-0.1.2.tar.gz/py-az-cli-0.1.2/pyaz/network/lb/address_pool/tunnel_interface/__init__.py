from ..... pyaz_utils import call_az

def add(address_pool, identifier, lb_name, protocol, resource_group, type, port=None):
    '''
    Add one tunnel interface into the load balance tunnel interface pool.
    '''
    return call_az("az network lb address-pool tunnel-interface add", locals())


def update(address_pool, index, lb_name, resource_group, identifier=None, port=None, protocol=None, type=None):
    '''
    update one tunnel interface of load balance tunnel interface pool.
    '''
    return call_az("az network lb address-pool tunnel-interface update", locals())


def remove(address_pool, index, lb_name, resource_group):
    '''
    Remove one tunnel interface from the load balance tunnel interface pool.
    '''
    return call_az("az network lb address-pool tunnel-interface remove", locals())


def list(address_pool, lb_name, resource_group):
    '''
    List all tunnel interfacees of the load balance tunnel interface pool.
    '''
    return call_az("az network lb address-pool tunnel-interface list", locals())


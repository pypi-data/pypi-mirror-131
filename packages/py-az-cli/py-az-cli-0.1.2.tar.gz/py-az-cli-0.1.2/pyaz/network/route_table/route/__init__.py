from .... pyaz_utils import call_az

def create(address_prefix, name, next_hop_type, resource_group, route_table_name, next_hop_ip_address=None):
    '''
    Create a route in a route table.
    '''
    return call_az("az network route-table route create", locals())


def delete(name, resource_group, route_table_name):
    '''
    Delete a route from a route table.
    '''
    return call_az("az network route-table route delete", locals())


def show(name, resource_group, route_table_name):
    '''
    Get the details of a route in a route table.
    '''
    return call_az("az network route-table route show", locals())


def list(resource_group, route_table_name):
    '''
    List routes in a route table.
    '''
    return call_az("az network route-table route list", locals())


def update(name, resource_group, route_table_name, add=None, address_prefix=None, force_string=None, next_hop_ip_address=None, next_hop_type=None, remove=None, set=None):
    '''
    Update a route in a route table.
    '''
    return call_az("az network route-table route update", locals())


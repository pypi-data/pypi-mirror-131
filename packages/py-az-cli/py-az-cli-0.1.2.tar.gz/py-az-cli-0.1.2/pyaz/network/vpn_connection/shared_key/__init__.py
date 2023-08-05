from .... pyaz_utils import call_az

def show(connection_name, resource_group):
    '''
    Retrieve a VPN connection shared key.
    '''
    return call_az("az network vpn-connection shared-key show", locals())


def reset(connection_name, key_length, resource_group=None):
    '''
    Reset a VPN connection shared key.
    '''
    return call_az("az network vpn-connection shared-key reset", locals())


def update(connection_name, resource_group, value, add=None, force_string=None, remove=None, set=None):
    '''
    Update a VPN connection shared key.
    '''
    return call_az("az network vpn-connection shared-key update", locals())


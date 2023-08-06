from .... pyaz_utils import _call_az

def show(resource_group, server):
    '''
    Gets a server's secure connection policy.
    '''
    return _call_az("az sql server conn-policy show", locals())


def update(connection_type, resource_group, server):
    '''
    Updates a server's secure connection policy.
    '''
    return _call_az("az sql server conn-policy update", locals())


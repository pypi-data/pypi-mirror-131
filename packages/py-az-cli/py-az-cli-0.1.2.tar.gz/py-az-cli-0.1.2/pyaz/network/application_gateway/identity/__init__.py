from .... pyaz_utils import call_az

def assign(gateway_name, identity, resource_group, no_wait=None):
    '''
    Assign a managed service identity to an application-gateway
    '''
    return call_az("az network application-gateway identity assign", locals())


def remove(gateway_name, resource_group, no_wait=None):
    '''
    Remove the managed service identity of an application-gateway
    '''
    return call_az("az network application-gateway identity remove", locals())


def show(gateway_name, resource_group):
    '''
    Show the managed service identity of an application-gateway
    '''
    return call_az("az network application-gateway identity show", locals())


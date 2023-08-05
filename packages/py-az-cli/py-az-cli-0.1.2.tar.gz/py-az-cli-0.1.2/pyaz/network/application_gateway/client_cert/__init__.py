from .... pyaz_utils import call_az

def add(data, gateway_name, name, resource_group):
    '''
    Add trusted client certificate of the application gateway.
    '''
    return call_az("az network application-gateway client-cert add", locals())


def remove(gateway_name, name, resource_group):
    '''
    Remove an existing trusted client certificate of the application gateway.
    '''
    return call_az("az network application-gateway client-cert remove", locals())


def list(gateway_name, resource_group):
    '''
    List the existing trusted client certificate of the application gateway.
    '''
    return call_az("az network application-gateway client-cert list", locals())


def show(gateway_name, name, resource_group):
    '''
    Show an existing trusted client certificate of the application gateway.
    '''
    return call_az("az network application-gateway client-cert show", locals())


def update(data, gateway_name, name, resource_group):
    '''
    Update trusted client certificate of the application gateway.
    '''
    return call_az("az network application-gateway client-cert update", locals())


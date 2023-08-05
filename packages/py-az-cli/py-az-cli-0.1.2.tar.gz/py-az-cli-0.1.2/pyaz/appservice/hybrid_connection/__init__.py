from ... pyaz_utils import call_az

def set_key(hybrid_connection, key_type, namespace, plan, resource_group):
    '''
    set the key that all apps in an appservice plan use to connect to the hybrid-connections in that appservice plan
    '''
    return call_az("az appservice hybrid-connection set-key", locals())


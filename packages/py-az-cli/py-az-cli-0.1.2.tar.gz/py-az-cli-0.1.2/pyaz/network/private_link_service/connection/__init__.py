from .... pyaz_utils import call_az

def delete(name, resource_group, service_name):
    '''
    Delete a private link service endpoint connection.
    '''
    return call_az("az network private-link-service connection delete", locals())


def update(connection_status, name, resource_group, service_name, action_required=None, description=None):
    '''
    Update a private link service endpoint connection.
    '''
    return call_az("az network private-link-service connection update", locals())


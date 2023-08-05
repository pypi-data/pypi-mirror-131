from ... pyaz_utils import call_az

def create(name, replication_role, resource_group, server_to_link):
    '''
    Adds a server link to the Redis cache (requires Premium SKU).
    '''
    return call_az("az redis server-link create", locals())


def delete(linked_server_name, name, resource_group):
    return call_az("az redis server-link delete", locals())


def show(linked_server_name, name, resource_group):
    return call_az("az redis server-link show", locals())


def list(name, resource_group):
    return call_az("az redis server-link list", locals())


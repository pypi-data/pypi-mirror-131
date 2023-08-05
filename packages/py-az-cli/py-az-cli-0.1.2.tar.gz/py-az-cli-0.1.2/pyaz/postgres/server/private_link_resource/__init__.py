from .... pyaz_utils import call_az

def list(resource_group, server_name):
    '''
    List the private link resources supported for a PostgreSQL server.
    '''
    return call_az("az postgres server private-link-resource list", locals())


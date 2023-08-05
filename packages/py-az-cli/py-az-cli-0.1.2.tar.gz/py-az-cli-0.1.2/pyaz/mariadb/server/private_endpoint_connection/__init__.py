from .... pyaz_utils import call_az

def approve(description=None, id=None, name=None, resource_group=None, server_name=None):
    '''
    Approve the specified private endpoint connection associated with a MariaDB server.
    '''
    return call_az("az mariadb server private-endpoint-connection approve", locals())


def reject(description=None, id=None, name=None, resource_group=None, server_name=None):
    '''
    Reject the specified private endpoint connection associated with a MariaDB server.
    '''
    return call_az("az mariadb server private-endpoint-connection reject", locals())


def delete(id=None, name=None, resource_group=None, server_name=None):
    '''
    Delete the specified private endpoint connection associated with a MariaDB server.
    '''
    return call_az("az mariadb server private-endpoint-connection delete", locals())


def show(id=None, name=None, resource_group=None, server_name=None):
    '''
    Show details of a private endpoint connection associated with a MariaDB server.
    '''
    return call_az("az mariadb server private-endpoint-connection show", locals())


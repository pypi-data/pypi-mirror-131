from .... pyaz_utils import call_az

def create(end_ip_address, name, resource_group, server_name, start_ip_address):
    '''
    Create a new firewall rule for a server.
    '''
    return call_az("az mariadb server firewall-rule create", locals())


def delete(name, resource_group, server_name, yes=None):
    '''
    Delete a firewall rule.
    '''
    return call_az("az mariadb server firewall-rule delete", locals())


def show(name, resource_group, server_name):
    '''
    Get the details of a firewall rule.
    '''
    return call_az("az mariadb server firewall-rule show", locals())


def list(resource_group, server_name):
    '''
    List all firewall rules for a server.
    '''
    return call_az("az mariadb server firewall-rule list", locals())


def update(name, resource_group, server_name, add=None, end_ip_address=None, force_string=None, remove=None, set=None, start_ip_address=None):
    '''
    Update a firewall rule.
    '''
    return call_az("az mariadb server firewall-rule update", locals())


from .... pyaz_utils import call_az

def create(name, resource_group, end_ip_address=None, rule_name=None, start_ip_address=None):
    '''
    Create a new firewall rule for a flexible server.
    '''
    return call_az("az postgres flexible-server firewall-rule create", locals())


def delete(name, resource_group, rule_name, yes=None):
    '''
    Delete a firewall rule.
    '''
    return call_az("az postgres flexible-server firewall-rule delete", locals())


def show(name, resource_group, rule_name):
    '''
    Get the details of a firewall rule.
    '''
    return call_az("az postgres flexible-server firewall-rule show", locals())


def list(name, resource_group):
    '''
    List all firewall rules for a flexible server.
    '''
    return call_az("az postgres flexible-server firewall-rule list", locals())


def update(name, resource_group, rule_name, add=None, end_ip_address=None, force_string=None, remove=None, set=None, start_ip_address=None):
    '''
    Update a firewall rule.
    '''
    return call_az("az postgres flexible-server firewall-rule update", locals())


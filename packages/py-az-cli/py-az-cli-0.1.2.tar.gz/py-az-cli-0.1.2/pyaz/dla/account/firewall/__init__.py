from .... pyaz_utils import call_az

def create(account, end_ip_address, firewall_rule_name, start_ip_address, resource_group=None):
    '''
    Create a firewall rule in a Data Lake Analytics account.
    '''
    return call_az("az dla account firewall create", locals())


def update(account, firewall_rule_name, end_ip_address=None, resource_group=None, start_ip_address=None):
    '''
    Update a firewall rule in a Data Lake Analytics account.
    '''
    return call_az("az dla account firewall update", locals())


def list(account, resource_group=None):
    '''
    List firewall rules in a Data Lake Analytics account.
    '''
    return call_az("az dla account firewall list", locals())


def show(account, firewall_rule_name, resource_group=None):
    '''
    Retrieve a firewall rule in a Data Lake Analytics account.
    '''
    return call_az("az dla account firewall show", locals())


def delete(account, firewall_rule_name, resource_group=None):
    '''
    Delete a firewall rule in a Data Lake Analytics account.
    '''
    return call_az("az dla account firewall delete", locals())


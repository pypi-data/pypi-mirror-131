from .... pyaz_utils import call_az

def create(account, end_ip_address, firewall_rule_name, start_ip_address, resource_group=None):
    '''
    Creates a firewall rule in a Data Lake Store account.
    '''
    return call_az("az dls account firewall create", locals())


def update(account, firewall_rule_name, end_ip_address=None, resource_group=None, start_ip_address=None):
    '''
    Updates a firewall rule in a Data Lake Store account.
    '''
    return call_az("az dls account firewall update", locals())


def list(account, resource_group=None):
    '''
    Lists firewall rules in a Data Lake Store account.
    '''
    return call_az("az dls account firewall list", locals())


def show(account, firewall_rule_name, resource_group=None):
    '''
    Get the details of a firewall rule in a Data Lake Store account.
    '''
    return call_az("az dls account firewall show", locals())


def delete(account, firewall_rule_name, resource_group=None):
    '''
    Deletes a firewall rule in a Data Lake Store account.
    '''
    return call_az("az dls account firewall delete", locals())


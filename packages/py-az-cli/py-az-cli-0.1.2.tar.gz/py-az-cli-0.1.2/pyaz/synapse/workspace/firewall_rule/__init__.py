from .... pyaz_utils import call_az

def list(resource_group, workspace_name):
    '''
    List all firewall rules.
    '''
    return call_az("az synapse workspace firewall-rule list", locals())


def show(name, resource_group, workspace_name):
    '''
    Get a firewall rule.
    '''
    return call_az("az synapse workspace firewall-rule show", locals())


def create(end_ip_address, name, resource_group, start_ip_address, workspace_name, no_wait=None):
    '''
    Create a firewall rule.
    '''
    return call_az("az synapse workspace firewall-rule create", locals())


def update(name, resource_group, workspace_name, end_ip_address=None, no_wait=None, start_ip_address=None):
    '''
    Update a firewall rule.
    '''
    return call_az("az synapse workspace firewall-rule update", locals())


def delete(name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Delete a firewall rule.
    '''
    return call_az("az synapse workspace firewall-rule delete", locals())


def wait(resource_group, rule_name, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a firewall rule is met.
    '''
    return call_az("az synapse workspace firewall-rule wait", locals())


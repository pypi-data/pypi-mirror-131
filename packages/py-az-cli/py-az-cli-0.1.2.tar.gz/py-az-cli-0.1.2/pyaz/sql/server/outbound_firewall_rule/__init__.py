from .... pyaz_utils import call_az

def create(outbound_rule_fqdn, resource_group, server):
    '''
    Create a new outbound firewall rule.
    '''
    return call_az("az sql server outbound-firewall-rule create", locals())


def delete(outbound_rule_fqdn, resource_group, server):
    '''
    Delete the outbound firewall rule.
    '''
    return call_az("az sql server outbound-firewall-rule delete", locals())


def show(outbound_rule_fqdn, resource_group, server):
    '''
    Show the details for an outbound firewall rule.
    '''
    return call_az("az sql server outbound-firewall-rule show", locals())


def list(resource_group, server):
    '''
    List a server's outbound firewall rules.
    '''
    return call_az("az sql server outbound-firewall-rule list", locals())


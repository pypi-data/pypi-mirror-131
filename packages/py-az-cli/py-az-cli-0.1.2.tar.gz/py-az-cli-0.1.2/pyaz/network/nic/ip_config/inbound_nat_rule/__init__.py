from ..... pyaz_utils import call_az

def add(inbound_nat_rule, ip_config_name, nic_name, resource_group, lb_name=None):
    '''
    Add an inbound NAT rule to an IP configuration.
    '''
    return call_az("az network nic ip-config inbound-nat-rule add", locals())


def remove(inbound_nat_rule, ip_config_name, nic_name, resource_group, lb_name=None):
    '''
    Remove an inbound NAT rule of an IP configuration.
    '''
    return call_az("az network nic ip-config inbound-nat-rule remove", locals())


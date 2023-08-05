from .... pyaz_utils import call_az

def set(enabled, gateway_name, resource_group, disabled_rule_groups=None, disabled_rules=None, exclusion=None, file_upload_limit=None, firewall_mode=None, max_request_body_size=None, no_wait=None, request_body_check=None, rule_set_type=None, rule_set_version=None):
    '''
    Update the firewall configuration of a web application.
    '''
    return call_az("az network application-gateway waf-config set", locals())


def show(gateway_name, resource_group):
    '''
    Get the firewall configuration of a web application.
    '''
    return call_az("az network application-gateway waf-config show", locals())


def list_rule_sets(group=None, type=None, version=None):
    '''
    Get information on available WAF rule sets, rule groups, and rule IDs.
    '''
    return call_az("az network application-gateway waf-config list-rule-sets", locals())


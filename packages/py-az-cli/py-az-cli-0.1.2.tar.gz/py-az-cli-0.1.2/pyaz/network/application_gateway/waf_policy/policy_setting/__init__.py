from ..... pyaz_utils import call_az

def list(policy_name, resource_group):
    '''
    List properties of a web application firewall global configuration.
    '''
    return call_az("az network application-gateway waf-policy policy-setting list", locals())


def update(policy_name, resource_group, add=None, file_upload_limit_in_mb=None, force_string=None, max_request_body_size_in_kb=None, mode=None, remove=None, request_body_check=None, set=None, state=None):
    '''
    Update properties of a web application firewall global configuration.
    '''
    return call_az("az network application-gateway waf-policy policy-setting update", locals())


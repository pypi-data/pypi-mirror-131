from ..... pyaz_utils import call_az

def create(gateway_name, resource_group, rule_name, rule_set_name, variable, ignore_case=None, negate=None, no_wait=None, pattern=None):
    '''
    Create a rewrite rule condition.
    '''
    return call_az("az network application-gateway rewrite-rule condition create", locals())


def show(gateway_name, resource_group, rule_name, rule_set_name, variable):
    '''
    Get the details of a rewrite rule condition.
    '''
    return call_az("az network application-gateway rewrite-rule condition show", locals())


def list(gateway_name, resource_group, rule_name, rule_set_name):
    '''
    List rewrite rule conditions.
    '''
    return call_az("az network application-gateway rewrite-rule condition list", locals())


def delete(gateway_name, resource_group, rule_name, rule_set_name, variable, no_wait=None):
    '''
    Delete a rewrite rule condition.
    '''
    return call_az("az network application-gateway rewrite-rule condition delete", locals())


def update(gateway_name, resource_group, rule_name, rule_set_name, variable, add=None, force_string=None, ignore_case=None, negate=None, no_wait=None, pattern=None, remove=None, set=None):
    '''
    Update a rewrite rule condition.
    '''
    return call_az("az network application-gateway rewrite-rule condition update", locals())


def list_server_variables():
    return call_az("az network application-gateway rewrite-rule condition list-server-variables", locals())


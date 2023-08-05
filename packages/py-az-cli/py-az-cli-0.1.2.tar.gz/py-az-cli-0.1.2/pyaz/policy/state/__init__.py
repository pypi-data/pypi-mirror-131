from ... pyaz_utils import call_az

def list(all=None, apply=None, expand=None, filter=None, from_=None, management_group=None, namespace=None, order_by=None, parent=None, policy_assignment=None, policy_definition=None, policy_set_definition=None, resource=None, resource_group=None, resource_type=None, select=None, to=None, top=None):
    '''
    List policy compliance states.
    '''
    return call_az("az policy state list", locals())


def summarize(filter=None, from_=None, management_group=None, namespace=None, parent=None, policy_assignment=None, policy_definition=None, policy_set_definition=None, resource=None, resource_group=None, resource_type=None, to=None, top=None):
    '''
    Summarize policy compliance states.
    '''
    return call_az("az policy state summarize", locals())


def trigger_scan(no_wait=None, resource_group=None):
    '''
    Trigger a policy compliance evaluation for a scope.
    '''
    return call_az("az policy state trigger-scan", locals())


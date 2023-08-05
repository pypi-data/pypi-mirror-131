from ... pyaz_utils import call_az

def list(apply=None, filter=None, from_=None, management_group=None, namespace=None, order_by=None, parent=None, policy_assignment=None, policy_definition=None, policy_set_definition=None, resource=None, resource_group=None, resource_type=None, select=None, to=None, top=None):
    '''
    List policy events.
    '''
    return call_az("az policy event list", locals())


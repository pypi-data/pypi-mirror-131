from .... pyaz_utils import call_az

def set(diffbackup_hours, name, resource_group, retention_days, server, no_wait=None):
    '''
    Update short term retention settings for a live database.
    '''
    return call_az("az sql db str-policy set", locals())


def show(name, resource_group, server):
    '''
    Show the short term retention policy for a live database.
    '''
    return call_az("az sql db str-policy show", locals())


def wait(name, policy_name, resource_group, server, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until the policy is set.
    '''
    return call_az("az sql db str-policy wait", locals())


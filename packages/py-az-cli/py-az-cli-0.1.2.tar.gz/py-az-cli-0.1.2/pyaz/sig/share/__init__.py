from ... pyaz_utils import call_az

def add(gallery_name, resource_group, no_wait=None, op_type=None, subscription_ids=None, tenant_ids=None):
    '''
    Share gallery with subscriptions and tenants
    '''
    return call_az("az sig share add", locals())


def remove(gallery_name, resource_group, no_wait=None, op_type=None, subscription_ids=None, tenant_ids=None):
    '''
    stop sharing gallery with a subscription or tenant
    '''
    return call_az("az sig share remove", locals())


def reset(gallery_name, resource_group, no_wait=None):
    '''
    disable gallery from being shared with subscription or tenant
    '''
    return call_az("az sig share reset", locals())


def wait(gallery_name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a shared gallery is met.
    '''
    return call_az("az sig share wait", locals())


from .... pyaz_utils import call_az

def show(name, resource_group, server):
    return call_az("az sql server dns-alias show", locals())


def list(resource_group, server):
    return call_az("az sql server dns-alias list", locals())


def create(name, resource_group, server):
    return call_az("az sql server dns-alias create", locals())


def delete(name, resource_group, server):
    return call_az("az sql server dns-alias delete", locals())


def set(name, original_server, resource_group, server, original_resource_group=None, original_subscription_id=None):
    '''
    Sets a server to which DNS alias should point
    '''
    return call_az("az sql server dns-alias set", locals())


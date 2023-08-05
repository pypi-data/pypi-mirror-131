from ... pyaz_utils import call_az

def create(group_member, location, name, resource_group, trust_scope, no_wait=None):
    '''
    Create a Server Trust Group.
    '''
    return call_az("az sql stg create", locals())


def delete(location, name, resource_group, no_wait=None, yes=None):
    '''
    Delete a Server Trust Group.
    '''
    return call_az("az sql stg delete", locals())


def show(location, name, resource_group):
    '''
    Retrieve a Server Trust Group.
    '''
    return call_az("az sql stg show", locals())


def list(resource_group, instance_name=None, location=None):
    '''
    Retrieve a list of Server Trust Groups.
    '''
    return call_az("az sql stg list", locals())


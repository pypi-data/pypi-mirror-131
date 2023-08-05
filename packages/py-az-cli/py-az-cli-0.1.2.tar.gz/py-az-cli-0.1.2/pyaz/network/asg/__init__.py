from ... pyaz_utils import call_az

def create(name, resource_group, location=None, tags=None):
    '''
    Create an application security group.
    '''
    return call_az("az network asg create", locals())


def show(name, resource_group):
    '''
    Get details of an application security group.
    '''
    return call_az("az network asg show", locals())


def list():
    '''
    List all application security groups in a subscription.
    '''
    return call_az("az network asg list", locals())


def delete(name, resource_group):
    '''
    Delete an application security group.
    '''
    return call_az("az network asg delete", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update an application security group.
    '''
    return call_az("az network asg update", locals())


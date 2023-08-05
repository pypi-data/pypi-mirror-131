from ... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Show the details of an action group
    '''
    return call_az("az monitor action-group show", locals())


def create(name, resource_group, action=None, short_name=None, tags=None):
    '''
    Create a new action group
    '''
    return call_az("az monitor action-group create", locals())


def delete(name, resource_group):
    return call_az("az monitor action-group delete", locals())


def enable_receiver(action_group, name, resource_group):
    '''
    Enable a receiver in an action group.
    '''
    return call_az("az monitor action-group enable-receiver", locals())


def list(resource_group=None):
    '''
    List action groups under a resource group or the current subscription
    '''
    return call_az("az monitor action-group list", locals())


def update(name, resource_group, add=None, add_action=None, force_string=None, remove=None, remove_action=None, set=None, short_name=None, tags=None):
    '''
    Update an action group
    '''
    return call_az("az monitor action-group update", locals())


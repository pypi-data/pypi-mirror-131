from ... pyaz_utils import call_az

def create(file, name, workspace_name, no_wait=None):
    '''
    Create a trigger.
    '''
    return call_az("az synapse trigger create", locals())


def set(file, name, workspace_name, no_wait=None):
    '''
    Update an exist trigger.
    '''
    return call_az("az synapse trigger set", locals())


def update(file, name, workspace_name, no_wait=None):
    '''
    Update an exist trigger.
    '''
    return call_az("az synapse trigger update", locals())


def list(workspace_name):
    '''
    List triggers.
    '''
    return call_az("az synapse trigger list", locals())


def show(name, workspace_name):
    '''
    Get a trigger.
    '''
    return call_az("az synapse trigger show", locals())


def delete(name, workspace_name, no_wait=None, yes=None):
    '''
    Delete a trigger.
    '''
    return call_az("az synapse trigger delete", locals())


def subscribe_to_event(name, workspace_name, no_wait=None):
    '''
    Subscribe event trigger to events.
    '''
    return call_az("az synapse trigger subscribe-to-event", locals())


def get_event_subscription_status(name, workspace_name):
    '''
    Get a trigger's event subscription status.
    '''
    return call_az("az synapse trigger get-event-subscription-status", locals())


def unsubscribe_from_event(name, workspace_name, no_wait=None):
    '''
    Unsubscribe event trigger from events.
    '''
    return call_az("az synapse trigger unsubscribe-from-event", locals())


def start(name, workspace_name, no_wait=None):
    '''
    Starts a trigger.
    '''
    return call_az("az synapse trigger start", locals())


def stop(name, workspace_name, no_wait=None):
    '''
    Stops a trigger.
    '''
    return call_az("az synapse trigger stop", locals())


def wait(name, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a trigger is met.
    '''
    return call_az("az synapse trigger wait", locals())


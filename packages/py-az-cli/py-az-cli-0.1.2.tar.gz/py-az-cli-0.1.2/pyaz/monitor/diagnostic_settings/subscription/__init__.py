from .... pyaz_utils import call_az

def create(location, logs, name, event_hub_auth_rule=None, event_hub_name=None, service_bus_rule=None, storage_account=None, workspace=None):
    '''
    Create diagnostic settings for a subscription
    '''
    return call_az("az monitor diagnostic-settings subscription create", locals())


def delete(name, subscription_id=None, yes=None):
    return call_az("az monitor diagnostic-settings subscription delete", locals())


def show(name, subscription_id=None):
    return call_az("az monitor diagnostic-settings subscription show", locals())


def list(subscription_id=None):
    return call_az("az monitor diagnostic-settings subscription list", locals())


def update(name, add=None, event_hub_auth_rule=None, event_hub_name=None, force_string=None, logs=None, remove=None, service_bus_rule=None, set=None, storage_account=None, subscription_id=None, workspace=None):
    '''
    Update diagnostic settings for a subscription.
    '''
    return call_az("az monitor diagnostic-settings subscription update", locals())


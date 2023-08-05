from ... pyaz_utils import call_az

def create(condition, name, target, action=None, description=None, disabled=None, email_service_owners=None, location=None, resource_group=None, tags=None, target_namespace=None, target_parent=None, target_type=None):
    '''
    Create a classic metric-based alert rule.
    '''
    return call_az("az monitor alert create", locals())


def delete(name, resource_group):
    '''
    Delete an alert rule.
    '''
    return call_az("az monitor alert delete", locals())


def show(name, resource_group):
    '''
    Show an alert rule.
    '''
    return call_az("az monitor alert show", locals())


def list(resource_group):
    '''
    List alert rules in a resource group.
    '''
    return call_az("az monitor alert list", locals())


def show_incident(name, resource_group, rule_name):
    '''
    Get the details of an alert rule incident.
    '''
    return call_az("az monitor alert show-incident", locals())


def list_incidents(resource_group, rule_name):
    '''
    List all incidents for an alert rule.
    '''
    return call_az("az monitor alert list-incidents", locals())


def update(name, add=None, add_action=None, aggregation=None, condition=None, description=None, email_service_owners=None, enabled=None, force_string=None, metric=None, operator=None, period=None, remove=None, remove_action=None, resource=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, set=None, tags=None, threshold=None):
    '''
    Update a classic metric-based alert rule.
    '''
    return call_az("az monitor alert update", locals())


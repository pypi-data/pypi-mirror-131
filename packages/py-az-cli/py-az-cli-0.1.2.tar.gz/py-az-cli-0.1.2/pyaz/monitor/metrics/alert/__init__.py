from .... pyaz_utils import call_az
from . import condition, dimension


def create(condition, name, resource_group, scopes, action=None, auto_mitigate=None, description=None, disabled=None, evaluation_frequency=None, severity=None, tags=None, target_resource_region=None, target_resource_type=None, window_size=None):
    '''
    Create a metric-based alert rule.
    '''
    return call_az("az monitor metrics alert create", locals())


def delete(name, resource_group):
    '''
    Delete a metrics-based alert rule.
    '''
    return call_az("az monitor metrics alert delete", locals())


def list(resource_group=None):
    '''
    List metric-based alert rules.
    '''
    return call_az("az monitor metrics alert list", locals())


def show(name, resource_group):
    '''
    Show a metrics-based alert rule.
    '''
    return call_az("az monitor metrics alert show", locals())


def update(name, resource_group, add=None, add_action=None, add_condition=None, auto_mitigate=None, description=None, enabled=None, evaluation_frequency=None, force_string=None, remove=None, remove_actions=None, remove_conditions=None, scopes=None, set=None, severity=None, tags=None, window_size=None):
    '''
    Update a metric-based alert rule.
    '''
    return call_az("az monitor metrics alert update", locals())


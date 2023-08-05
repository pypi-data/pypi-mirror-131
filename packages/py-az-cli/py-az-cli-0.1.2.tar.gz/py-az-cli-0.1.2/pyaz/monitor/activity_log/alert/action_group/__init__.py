from ..... pyaz_utils import call_az

def add(action_group, name, resource_group, reset=None, strict=None, webhook_properties=None):
    '''
    Add action groups to this activity log alert. It can also be used to overwrite existing webhook properties of particular action groups.
    '''
    return call_az("az monitor activity-log alert action-group add", locals())


def remove(action_group, name, resource_group):
    '''
    Remove action groups from this activity log alert
    '''
    return call_az("az monitor activity-log alert action-group remove", locals())


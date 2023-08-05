from .... pyaz_utils import call_az

def create(autoscale_name, condition, scale, cooldown=None, profile_name=None, resource=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, timegrain=None):
    '''
    Add a new autoscale rule.
    '''
    return call_az("az monitor autoscale rule create", locals())


def list(autoscale_name, resource_group, profile_name=None):
    '''
    List autoscale rules for a profile.
    '''
    return call_az("az monitor autoscale rule list", locals())


def delete(autoscale_name, index, resource_group, profile_name=None):
    '''
    Remove autoscale rules from a profile.
    '''
    return call_az("az monitor autoscale rule delete", locals())


def copy(autoscale_name, dest_schedule, index, resource_group, source_schedule=None):
    '''
    Copy autoscale rules from one profile to another.
    '''
    return call_az("az monitor autoscale rule copy", locals())


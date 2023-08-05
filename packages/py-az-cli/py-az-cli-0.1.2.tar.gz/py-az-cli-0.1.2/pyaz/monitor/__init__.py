from .. pyaz_utils import call_az
from . import action_group, activity_log, alert, autoscale, autoscale_settings, diagnostic_settings, log_profiles, metrics, private_link_scope


def clone(source_resource, target_resource, always_clone=None, types=None):
    '''
    Clone metrics alert rules from one resource to another resource.
    '''
    return call_az("az monitor clone", locals())


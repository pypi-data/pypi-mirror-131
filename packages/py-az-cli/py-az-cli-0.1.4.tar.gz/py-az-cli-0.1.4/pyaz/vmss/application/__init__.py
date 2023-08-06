from ... pyaz_utils import _call_az

def set(app_version_ids, name, resource_group, app_config_overrides=None, order_applications=None):
    '''
    Set applications for VMSS.
    '''
    return _call_az("az vmss application set", locals())


def list(name, resource_group):
    '''
    List applications for VMSS
    '''
    return _call_az("az vmss application list", locals())


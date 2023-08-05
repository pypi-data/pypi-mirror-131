from ... pyaz_utils import call_az

def set(resource_group, settings, vmss_name, no_auto_upgrade_minor_version=None, protected_settings=None, version=None):
    '''
    Enable diagnostics on a VMSS.
    '''
    return call_az("az vmss diagnostics set", locals())


def get_default_config(is_windows_os=None):
    '''
    Show the default config file which defines data to be collected.
    '''
    return call_az("az vmss diagnostics get-default-config", locals())


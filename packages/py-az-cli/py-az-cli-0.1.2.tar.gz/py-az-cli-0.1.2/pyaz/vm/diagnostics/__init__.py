from ... pyaz_utils import call_az

def set(resource_group, settings, vm_name, no_auto_upgrade_minor_version=None, protected_settings=None, version=None):
    '''
    Configure the Azure VM diagnostics extension.
    '''
    return call_az("az vm diagnostics set", locals())


def get_default_config(is_windows_os=None):
    '''
    Get the default configuration settings for a VM.
    '''
    return call_az("az vm diagnostics get-default-config", locals())


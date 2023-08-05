from ... pyaz_utils import call_az

def disable(name, resource_group):
    '''
    Disable the boot diagnostics on a VM.
    '''
    return call_az("az vm boot-diagnostics disable", locals())


def enable(name, resource_group, storage=None):
    '''
    Enable the boot diagnostics on a VM.
    '''
    return call_az("az vm boot-diagnostics enable", locals())


def get_boot_log(name, resource_group):
    '''
    Get the boot diagnostics log from a VM.
    '''
    return call_az("az vm boot-diagnostics get-boot-log", locals())


def get_boot_log_uris(name, resource_group, expire=None):
    '''
    Get SAS URIs for a virtual machine's boot diagnostic logs.
    '''
    return call_az("az vm boot-diagnostics get-boot-log-uris", locals())


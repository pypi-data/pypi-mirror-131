from ... pyaz_utils import call_az

def list(resource_group, vault_name, backup_management_type=None, end_date=None, operation=None, start_date=None, status=None, use_secondary_region=None):
    '''
    List all backup jobs of a Recovery Services vault.
    '''
    return call_az("az backup job list", locals())


def show(name, resource_group, vault_name, use_secondary_region=None):
    '''
    Show details of a particular job.
    '''
    return call_az("az backup job show", locals())


def stop(name, resource_group, vault_name, use_secondary_region=None):
    '''
    Suspend or terminate a currently running job.
    '''
    return call_az("az backup job stop", locals())


def wait(name, resource_group, vault_name, timeout=None, use_secondary_region=None):
    '''
    Wait until either the job completes or the specified timeout value is reached.
    '''
    return call_az("az backup job wait", locals())


from .... pyaz_utils import call_az

def show(account_name, backup_policy_name, resource_group):
    '''
    Get the specified ANF backup policy.
    '''
    return call_az("az netappfiles account backup-policy show", locals())


def list(account_name, resource_group):
    '''
    List the ANF backup policy for the specified account.
    '''
    return call_az("az netappfiles account backup-policy list", locals())


def delete(account_name, backup_policy_name, resource_group):
    '''
    Delete the specified ANF backup policy.
    '''
    return call_az("az netappfiles account backup-policy delete", locals())


def update(account_name, backup_policy_name, resource_group, daily_backups=None, enabled=None, location=None, monthly_backups=None, tags=None, weekly_backups=None):
    '''
    Update the specified ANF backup policy.
    '''
    return call_az("az netappfiles account backup-policy update", locals())


def create(account_name, backup_policy_name, location, resource_group, daily_backups=None, enabled=None, monthly_backups=None, tags=None, weekly_backups=None):
    '''
    Create a new Azure NetApp Files (ANF) backup policy.
    '''
    return call_az("az netappfiles account backup-policy create", locals())


from .... pyaz_utils import call_az

def show(account_name, resource_group, snapshot_policy_name):
    '''
    Get the specified ANF snapshot policy.
    '''
    return call_az("az netappfiles snapshot policy show", locals())


def list(account_name, resource_group):
    '''
    List the ANF snapshot policies for the specified account.
    '''
    return call_az("az netappfiles snapshot policy list", locals())


def volumes(account_name, resource_group, snapshot_policy_name):
    '''
    Get the all ANF volumes associated with snapshot policy.
    '''
    return call_az("az netappfiles snapshot policy volumes", locals())


def delete(account_name, resource_group, snapshot_policy_name):
    '''
    Delete the specified ANF snapshot policy.
    '''
    return call_az("az netappfiles snapshot policy delete", locals())


def update(account_name, location, resource_group, snapshot_policy_name, daily_hour=None, daily_minute=None, daily_snapshots=None, enabled=None, hourly_minute=None, hourly_snapshots=None, monthly_days=None, monthly_hour=None, monthly_minute=None, monthly_snapshots=None, weekly_day=None, weekly_hour=None, weekly_minute=None, weekly_snapshots=None):
    '''
    Update the specified ANF snapshot policy.
    '''
    return call_az("az netappfiles snapshot policy update", locals())


def create(account_name, location, resource_group, snapshot_policy_name, daily_hour=None, daily_minute=None, daily_snapshots=None, enabled=None, hourly_minute=None, hourly_snapshots=None, monthly_days=None, monthly_hour=None, monthly_minute=None, monthly_snapshots=None, tags=None, weekly_day=None, weekly_hour=None, weekly_minute=None, weekly_snapshots=None):
    '''
    Create a new Azure NetApp Files (ANF) snapshot policy.
    '''
    return call_az("az netappfiles snapshot policy create", locals())


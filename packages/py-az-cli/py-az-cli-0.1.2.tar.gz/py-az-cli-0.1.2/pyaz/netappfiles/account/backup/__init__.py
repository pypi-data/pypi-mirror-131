from .... pyaz_utils import call_az

def show(account_name, backup_name, resource_group):
    '''
    Get Backup for a Netapp Files (ANF) Account.
    '''
    return call_az("az netappfiles account backup show", locals())


def list(account_name, resource_group):
    '''
    Get list of all Azure NetApp Files (ANF) Account Backups.
    '''
    return call_az("az netappfiles account backup list", locals())


def delete(account_name, backup_name, resource_group, yes=None):
    '''
    Delete Backup for a Netapp Files (ANF) Account.
    '''
    return call_az("az netappfiles account backup delete", locals())


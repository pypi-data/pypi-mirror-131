from .... pyaz_utils import call_az

def show(account, storage_account_name, resource_group=None):
    return call_az("az dla account blob-storage show", locals())


def add(access_key, account, storage_account_name, resource_group=None, suffix=None):
    '''
    Links an Azure Storage account to the specified Data Lake Analytics account.
    '''
    return call_az("az dla account blob-storage add", locals())


def update(access_key, account, storage_account_name, resource_group=None, suffix=None):
    '''
    Updates an Azure Storage account linked to the specified Data Lake Analytics account.
    '''
    return call_az("az dla account blob-storage update", locals())


def delete(account, storage_account_name, resource_group=None):
    return call_az("az dla account blob-storage delete", locals())


def list(account, count=None, filter=None, orderby=None, resource_group=None, select=None, skip=None, top=None):
    return call_az("az dla account blob-storage list", locals())


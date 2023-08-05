from .... pyaz_utils import call_az

def show(account, data_lake_store_account_name, resource_group=None):
    return call_az("az dla account data-lake-store show", locals())


def list(account, count=None, filter=None, orderby=None, resource_group=None, select=None, skip=None, top=None):
    return call_az("az dla account data-lake-store list", locals())


def add(account, data_lake_store_account_name, resource_group=None, suffix=None):
    return call_az("az dla account data-lake-store add", locals())


def delete(account, data_lake_store_account_name, resource_group=None):
    return call_az("az dla account data-lake-store delete", locals())


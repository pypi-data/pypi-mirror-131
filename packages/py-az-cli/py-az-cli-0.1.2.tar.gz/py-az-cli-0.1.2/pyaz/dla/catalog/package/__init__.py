from .... pyaz_utils import call_az

def show(account, database_name, package_name, schema_name):
    return call_az("az dla catalog package show", locals())


def list(account, database_name, schema_name, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return call_az("az dla catalog package list", locals())


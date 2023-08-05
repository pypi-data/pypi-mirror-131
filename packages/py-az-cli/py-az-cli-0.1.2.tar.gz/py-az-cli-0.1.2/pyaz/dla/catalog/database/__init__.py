from .... pyaz_utils import call_az

def show(account, database_name):
    return call_az("az dla catalog database show", locals())


def list(account, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return call_az("az dla catalog database list", locals())


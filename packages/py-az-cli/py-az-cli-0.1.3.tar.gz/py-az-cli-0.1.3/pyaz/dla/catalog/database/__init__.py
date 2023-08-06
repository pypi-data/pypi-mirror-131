from .... pyaz_utils import _call_az

def show(account, database_name):
    return _call_az("az dla catalog database show", locals())


def list(account, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return _call_az("az dla catalog database list", locals())


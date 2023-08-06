from .... pyaz_utils import _call_az

def show(account, assembly_name, database_name):
    return _call_az("az dla catalog assembly show", locals())


def list(account, database_name, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return _call_az("az dla catalog assembly list", locals())


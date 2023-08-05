from .... pyaz_utils import call_az

def show(account, assembly_name, database_name):
    return call_az("az dla catalog assembly show", locals())


def list(account, database_name, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return call_az("az dla catalog assembly list", locals())


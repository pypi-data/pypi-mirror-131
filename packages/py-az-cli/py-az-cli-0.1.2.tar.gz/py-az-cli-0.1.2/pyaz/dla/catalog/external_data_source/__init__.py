from .... pyaz_utils import call_az

def show(account, database_name, external_data_source_name):
    return call_az("az dla catalog external-data-source show", locals())


def list(account, database_name, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    return call_az("az dla catalog external-data-source list", locals())


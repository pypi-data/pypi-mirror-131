from .... pyaz_utils import _call_az

def show(account, database_name, schema_name, statistics_name, table_name):
    return _call_az("az dla catalog table-stats show", locals())


def list(account, database_name, schema_name=None, table_name=None):
    '''
    List table statistics in a database, table, or schema.
    '''
    return _call_az("az dla catalog table-stats list", locals())


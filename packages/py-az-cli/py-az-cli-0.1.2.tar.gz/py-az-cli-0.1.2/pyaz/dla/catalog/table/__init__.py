from .... pyaz_utils import call_az

def show(account, database_name, schema_name, table_name):
    return call_az("az dla catalog table show", locals())


def list(account, database_name, schema_name=None):
    '''
    List tables in a database or schema.
    '''
    return call_az("az dla catalog table list", locals())


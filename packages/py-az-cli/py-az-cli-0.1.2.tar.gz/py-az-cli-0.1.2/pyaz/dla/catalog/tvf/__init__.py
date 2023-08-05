from .... pyaz_utils import call_az

def show(account, database_name, schema_name, table_valued_function_name):
    return call_az("az dla catalog tvf show", locals())


def list(account, database_name, schema_name=None):
    '''
    List table valued functions in a database or schema.
    '''
    return call_az("az dla catalog tvf list", locals())


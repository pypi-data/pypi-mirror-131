from ... pyaz_utils import call_az

def query(table_name, accept=None, account_key=None, account_name=None, connection_string=None, filter=None, marker=None, num_results=None, sas_token=None, select=None, timeout=None):
    '''
    List entities which satisfy a query.
    '''
    return call_az("az storage entity query", locals())


def replace(entity, table_name, account_key=None, account_name=None, connection_string=None, if_match=None, sas_token=None, timeout=None):
    return call_az("az storage entity replace", locals())


def merge(entity, table_name, account_key=None, account_name=None, connection_string=None, if_match=None, sas_token=None, timeout=None):
    return call_az("az storage entity merge", locals())


def delete(partition_key, row_key, table_name, account_key=None, account_name=None, connection_string=None, if_match=None, sas_token=None, timeout=None):
    return call_az("az storage entity delete", locals())


def show(partition_key, row_key, table_name, accept=None, account_key=None, account_name=None, connection_string=None, sas_token=None, select=None, timeout=None):
    return call_az("az storage entity show", locals())


def insert(entity, table_name, account_key=None, account_name=None, connection_string=None, if_exists=None, sas_token=None, timeout=None):
    '''
    Insert an entity into a table.
    '''
    return call_az("az storage entity insert", locals())


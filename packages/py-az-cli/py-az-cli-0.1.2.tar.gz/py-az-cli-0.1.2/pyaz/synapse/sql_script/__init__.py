from ... pyaz_utils import call_az

def list(workspace_name):
    '''
    List SQL scripts in a synapse workspace.
    '''
    return call_az("az synapse sql-script list", locals())


def show(name, workspace_name):
    '''
    Get a SQL script.
    '''
    return call_az("az synapse sql-script show", locals())


def delete(name, workspace_name, no_wait=None):
    '''
    Delete a SQL script.
    '''
    return call_az("az synapse sql-script delete", locals())


def create(file, name, workspace_name, additional_properties=None, description=None, folder_name=None, no_wait=None, result_limit=None, sql_database_name=None, sql_pool_name=None):
    '''
    Create or update a SQL script.
    '''
    return call_az("az synapse sql-script create", locals())


def wait(name, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a sql script is met.
    '''
    return call_az("az synapse sql-script wait", locals())


def export(output_folder, workspace_name, name=None):
    '''
    Export a SQL script.
    '''
    return call_az("az synapse sql-script export", locals())


def import_(file, name, workspace_name, additional_properties=None, description=None, folder_name=None, no_wait=None, result_limit=None, sql_database_name=None, sql_pool_name=None):
    '''
    Import a SQL script.
    '''
    return call_az("az synapse sql-script import", locals())


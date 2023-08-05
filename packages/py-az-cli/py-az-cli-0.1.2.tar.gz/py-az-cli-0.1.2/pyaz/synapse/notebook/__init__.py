from ... pyaz_utils import call_az

def create(file, name, workspace_name, executor_count=None, executor_size=None, folder_path=None, no_wait=None, spark_pool_name=None):
    '''
    Create a notebook.
    '''
    return call_az("az synapse notebook create", locals())


def set(file, name, workspace_name, executor_count=None, executor_size=None, folder_path=None, no_wait=None, spark_pool_name=None):
    '''
    Set an exist notebook.
    '''
    return call_az("az synapse notebook set", locals())


def import_(file, name, workspace_name, executor_count=None, executor_size=None, folder_path=None, no_wait=None, spark_pool_name=None):
    '''
    Import a notebook.
    '''
    return call_az("az synapse notebook import", locals())


def list(workspace_name):
    '''
    List notebooks.
    '''
    return call_az("az synapse notebook list", locals())


def show(name, workspace_name):
    '''
    Get a notebook.
    '''
    return call_az("az synapse notebook show", locals())


def export(output_folder, workspace_name, name=None):
    '''
    Export notebooks.
    '''
    return call_az("az synapse notebook export", locals())


def delete(name, workspace_name, no_wait=None, yes=None):
    '''
    Delete a notebook.
    '''
    return call_az("az synapse notebook delete", locals())


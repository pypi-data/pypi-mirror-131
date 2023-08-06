from .... pyaz_utils import _call_az

def delete(file_path, node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, recursive=None, yes=None):
    return _call_az("az batch node file delete", locals())


def download(destination, file_path, node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, end_range=None, if_modified_since=None, if_unmodified_since=None, start_range=None):
    '''
    Download the content of the a node file.
    '''
    return _call_az("az batch node file download", locals())


def show(file_path, node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, if_modified_since=None, if_unmodified_since=None):
    return _call_az("az batch node file show", locals())


def list(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, filter=None, recursive=None):
    return _call_az("az batch node file list", locals())


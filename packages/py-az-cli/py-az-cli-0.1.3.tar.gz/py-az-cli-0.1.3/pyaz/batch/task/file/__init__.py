from .... pyaz_utils import _call_az

def delete(file_path, job_id, task_id, account_endpoint=None, account_key=None, account_name=None, recursive=None, yes=None):
    return _call_az("az batch task file delete", locals())


def download(destination, file_path, job_id, task_id, account_endpoint=None, account_key=None, account_name=None, end_range=None, if_modified_since=None, if_unmodified_since=None, start_range=None):
    '''
    Download the content of a Batch task file.
    '''
    return _call_az("az batch task file download", locals())


def show(file_path, job_id, task_id, account_endpoint=None, account_key=None, account_name=None, if_modified_since=None, if_unmodified_since=None):
    return _call_az("az batch task file show", locals())


def list(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, filter=None, recursive=None):
    return _call_az("az batch task file list", locals())


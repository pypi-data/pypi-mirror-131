from ... pyaz_utils import call_az
from . import access


def show(account, path):
    '''
    Get file or folder information in a Data Lake Store account.
    '''
    return call_az("az dls fs show", locals())


def list(account, path):
    '''
    List the files and folders in a Data Lake Store account.
    '''
    return call_az("az dls fs list", locals())


def create(account, path, content=None, folder=None, force=None):
    '''
    Creates a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs create", locals())


def append(account, content, path):
    '''
    Append content to a file in a Data Lake Store account.
    '''
    return call_az("az dls fs append", locals())


def delete(account, path, recurse=None):
    '''
    Delete a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs delete", locals())


def upload(account, destination_path, source_path, block_size=None, buffer_size=None, chunk_size=None, overwrite=None, thread_count=None):
    '''
    Upload a file or folder to a Data Lake Store account.
    '''
    return call_az("az dls fs upload", locals())


def download(account, destination_path, source_path, block_size=None, buffer_size=None, chunk_size=None, overwrite=None, thread_count=None):
    '''
    Download a file or folder from a Data Lake Store account to the local machine.
    '''
    return call_az("az dls fs download", locals())


def test(account, path):
    '''
    Test for the existence of a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs test", locals())


def preview(account, path, force=None, length=None, offset=None):
    '''
    Preview the content of a file in a Data Lake Store account.
    '''
    return call_az("az dls fs preview", locals())


def join(account, destination_path, source_paths, force=None):
    '''
    Join files in a Data Lake Store account into one file.
    '''
    return call_az("az dls fs join", locals())


def move(account, destination_path, source_path, force=None):
    '''
    Move a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs move", locals())


def set_expiry(account, expiration_time, path):
    '''
    Set the expiration time for a file.
    '''
    return call_az("az dls fs set-expiry", locals())


def remove_expiry(account, path):
    '''
    Remove the expiration time for a file.
    '''
    return call_az("az dls fs remove-expiry", locals())


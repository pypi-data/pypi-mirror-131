from .... pyaz_utils import call_az

def list(experiment, job, resource_group, workspace, expiry=None, output_directory_id=None, path=None):
    '''
    List job's output files in a directory with given id.
    '''
    return call_az("az batchai job file list", locals())


def stream(experiment, file_name, job, resource_group, workspace, output_directory_id=None, path=None):
    '''
    Stream the content of a file (similar to 'tail -f').
    '''
    return call_az("az batchai job file stream", locals())


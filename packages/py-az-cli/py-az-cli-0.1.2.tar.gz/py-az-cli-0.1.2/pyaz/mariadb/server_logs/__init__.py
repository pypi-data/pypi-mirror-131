from ... pyaz_utils import call_az

def list(resource_group, server_name, file_last_written=None, filename_contains=None, max_file_size=None):
    '''
    List log files for a server.
    '''
    return call_az("az mariadb server-logs list", locals())


def download(name, resource_group, server_name):
    '''
    Download log files.
    '''
    return call_az("az mariadb server-logs download", locals())


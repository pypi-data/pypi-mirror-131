from .... pyaz_utils import call_az

def setup(admin_password, admin_user, database_name, repo, resource_group, server_name, sql_file, action_name=None, allow_push=None, branch=None):
    '''
    Create github action workflow file for PostgreSQL server.
    '''
    return call_az("az postgres flexible-server deploy setup", locals())


def run(action_name, branch):
    '''
    Run an existing workflow in your github repository
    '''
    return call_az("az postgres flexible-server deploy run", locals())


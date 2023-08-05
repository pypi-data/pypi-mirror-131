from .... pyaz_utils import call_az

def create(name, properties, resource_group, migration_name=None):
    '''
    Create a new migration workflow for a flexible server.
    '''
    return call_az("az postgres flexible-server migration create", locals())


def show(migration_name, name, resource_group, level=None):
    '''
    Get the details of a specific migration.
    '''
    return call_az("az postgres flexible-server migration show", locals())


def list(name, resource_group, filter=None):
    '''
    List the migrations of a flexible server.
    '''
    return call_az("az postgres flexible-server migration list", locals())


def update(migration_name, name, resource_group, cutover=None, db_names=None, overwrite_dbs=None, setup_replication=None, start_data_migration=None):
    '''
    Update a specific migration.
    '''
    return call_az("az postgres flexible-server migration update", locals())


def delete(migration_name, name, resource_group, yes=None):
    '''
    Delete a specific migration.
    '''
    return call_az("az postgres flexible-server migration delete", locals())


def check_name_availability(migration_name, name, resource_group):
    '''
    Checks if the provided migration-name can be used.
    '''
    return call_az("az postgres flexible-server migration check-name-availability", locals())


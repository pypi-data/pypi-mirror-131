from ... pyaz_utils import call_az
from . import container, database, restorable_container, restorable_database, restorable_resource, stored_procedure, trigger, user_defined_function


def retrieve_latest_backup_time(account_name, container_name, database_name, location, resource_group):
    '''
    Retrieves latest restorable timestamp for the given sql container in given region.
    '''
    return call_az("az cosmosdb sql retrieve-latest-backup-time", locals())


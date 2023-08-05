from ... pyaz_utils import call_az
from . import collection, database, restorable_collection, restorable_database, restorable_resource


def retrieve_latest_backup_time(account_name, collection_name, database_name, location, resource_group):
    '''
    Retrieves latest restorable timestamp for the given mongodb collection in given region.
    '''
    return call_az("az cosmosdb mongodb retrieve-latest-backup-time", locals())

